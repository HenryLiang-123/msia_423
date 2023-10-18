"""
This module provides utility functions for loading machine learning models from joblib files and 
loading data from CSV files into pandas DataFrames. It leverages Streamlit's caching mechanisms 
to optimize performance by preventing redundant file loading. The module also includes 
configurations for logging.

Functions:
    load_model: This function loads a machine learning model from a specified joblib file. 
                The loaded model is returned.

    load_data: This function loads data from a specified CSV file into a pandas DataFrame. 
               The loaded DataFrame is returned.
"""
import argparse
from pathlib import Path
import logging
from typing import Any
import joblib
import pandas as pd
import streamlit as st
import yaml


logger = logging.getLogger("clouds")

@st.cache_resource
def load_model(model_file: Path) -> Any:
    """
    Load a model from a joblib file.

    Args:
        model_file (Path): The path to the joblib file.

    Returns:
        Any: The loaded model object.
    """
    try:
        model = joblib.load(model_file)
        logger.info("Model successfully loaded as object")
        return model
    except Exception as e_1:
        logger.error("Failed to load model object")
        raise NotImplementedError from e_1

@st.cache_data
def load_data(data_path: Path) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file.

    Args:
        data_path (Path): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    try:
        dat = pd.read_csv(data_path)
        logger.info("Successfully loaded data into memory")
        return dat
    except Exception as e_1:
        logger.error("Failed to load data into memory")
        raise NotImplementedError from e_1
    
@st.cache_data
def load_config(config_path: Path) -> Any:
    """
    Loads a configuration file and returns the contents.

    This function opens a configuration file from a specified path, loads
    it into a Python object, and then returns this object. If there is a
    YAML error during loading, it raises a NotImplementedError and logs
    an error message.

    Args:
        config_path (Path): The path to the configuration file.

    Returns:
        config (Any): The Python object that the YAML file was loaded into.

    Raises:
        NotImplementedError: If there was an error loading the YAML file.
    """
    # Load configuration file for parameters and run config
    with open(config_path, "r") as file:
        try:
            config = yaml.load(file, Loader=yaml.FullLoader)
            logger.info("Configuration file loaded from %s", config_path)
        except yaml.error.YAMLError as e_0:
            logger.error("Error while loading configuration from %s", config_path)
            raise NotImplementedError from e_0
    
    return config