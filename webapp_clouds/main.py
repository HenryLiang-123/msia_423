"""
This module provides the main functionality of a cloud data processing and prediction pipeline.
It enables the user to perform multiple operations such as:
- Configuration loading for controlling runtime behaviour.
- Fetching of the model and data files from AWS S3 storage.
- Loading models from local files.
- Loading training data.
- Running the application using the Streamlit framework.
- Enabling user to select models and input feature values through the sidebar.
- Predicting the output of the model based on user inputs.

Functions:
    main: The main function of the script. It orchestrates the process of loading configurations,
          downloading models and data from S3, loading models and data into memory, running the 
          Streamlit application, and handling prediction logic.
"""
import logging.config
from pathlib import Path
import os
import pandas as pd
import streamlit as st
import src.aws_utils as aws
import src.utils as utl

logging.config.fileConfig("config/logging/local.conf", disable_existing_loggers=True)
logger = logging.getLogger("clouds")

def main():
    """
    The main function of the script.

    This function is responsible for loading configurations, downloading models and data from 
    AWS S3, loading models and data into memory, and orchestrating the execution of the 
    Streamlit application.

    It parses command-line arguments for the configuration file path. This configuration
    file controls runtime parameters such as AWS S3 bucket details and local storage
    directories.

    Once configurations are loaded, it downloads specified models and data files from AWS S3
    to local directories.

    It then loads the models and data into memory. The Streamlit application is then launched.

    The Streamlit application allows users to select a model and adjust feature input values.
    Based on these inputs, the selected model generates predictions.

    Note:
        This function assumes that the min, max, and default values for features are
        known and uses these for rendering sliders on the Streamlit sidebar.

    Args:
        --config (str): Optional command-line argument specifying the path to the
        configuration file. Default is 'config/config.yaml'.

    Raises:
        NotImplementedError: If there is an error while loading the configuration,
        selecting the model, or generating new predictions, a NotImplementedError is raised.
    """
    
    config = utl.load_config("config/config.yaml")
    run_config = config.get("run_config", {})

    # Download model from S3
    model_dir = Path(run_config["model_dir"])
    data_dir = Path(run_config["data_dir"])

    # Make dir if not exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    aws.download_s3(
        config["aws"]["model_bucket"],
        config["model_config"]["model1"][0]["name"],
        model_dir / config["model_config"]["model1"][0]["name"],
    )
    aws.download_s3(
        config["aws"]["model_bucket"],
        config["model_config"]["model2"][0]["name"],
        model_dir / config["model_config"]["model2"][0]["name"],
    )
    aws.download_s3(
        config["aws"]["model_bucket"],
        config["model_config"]["data"],
        data_dir / config["model_config"]["data"],
    )

    # Load data
    train_path = Path(data_dir) / "train.csv"

    train_df = utl.load_data(train_path)

    st.title("Model prediction")
    st.sidebar.header("Feature inputs")
    try:
        model_selection = st.sidebar.selectbox(
            "Select model", options=["Model 1", "Model 2"]
        )
        if model_selection == "Model 1":
            model = utl.load_model(Path(model_dir) / config["model_config"]["model1"][0]["name"])
            model_selection = "model1"
        elif model_selection == "Model 2":
            model = utl.load_model(Path(model_dir) / config["model_config"]["model2"][0]["name"])
            model_selection = "model2"

        logger.info("Model %s selected", model_selection)
    except Exception as e_1:
        logger.error("Failed to select model")
        raise NotImplementedError from e_1

    user_input = {}

    for feature in config["model_config"][model_selection][1]["features"]:
        # Assuming the min_value, max_value and default_value are known
        min_value = float(train_df[feature].min())
        max_value = float(train_df[feature].max())
        default_value = float(train_df[feature].mean())

        user_input[feature] = st.sidebar.slider(
            feature, min_value, max_value, default_value
        )

    # After getting all inputs, predict with the selected model and show on main page

    try:
        if st.sidebar.button("Submit"):
            df_input = pd.DataFrame([user_input])
            prediction = model.predict(df_input)
            st.session_state["prediction"] = prediction
            logger.info("New prediction request submitted")
        if "prediction" in st.session_state:
            st.write(
                f'The prediction from {model_selection} is: {st.session_state["prediction"]}'
            )
    except Exception as e_2:
        logger.error("Failed to generate new predictions")
        raise NotImplementedError from e_2


if __name__ == "__main__":
    main()
