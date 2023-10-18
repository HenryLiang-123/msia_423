from importlib import import_module
from pathlib import Path
import os
import pickle
from typing import Tuple
import logging
import pandas as pd
import sklearn

logger = logging.getLogger("clouds")


def train_model(
    data: pd.DataFrame, config: dict
) -> Tuple[object, pd.DataFrame, pd.DataFrame]:
    """train model
    Args:
        Args:
        data (pd.DataFrame): data for the model to be trained on
        config (dict): config file for model training

    Returns:
        None
    """

    features = data[config["initial_features"]]
    target = data[config["target"]]
    model_config = config["model_config"]

    # Import needed modules
    model_lib = import_module(model_config["model_lib"])

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        features, target, test_size=config["train_test_split"]["test_size"]
    )

    # Create model instance with hyperparameters
    try:
        model_class = getattr(model_lib, model_config["type"])
        model = model_class(**model_config["hyperparam"])
        model.fit(x_train, y_train)
        logger.info("Model successfully trained")
    except Exception as e:
        logger.error(
            "Model could not be instantiated due to %s. Please check the formatting of config.yaml",
            e,
        )
        raise NotImplementedError from e

    # Train and test datasets
    train = x_train
    train[config["target"]] = y_train

    test = x_test
    test[config["target"]] = y_test
    logger.info("Train and test sets created")

    return model, pd.DataFrame(train), pd.DataFrame(test)


def save_data(train: pd.DataFrame, test: pd.DataFrame, path: Path) -> None:
    """save train and test data to directory
    Args:
        Args:
        train (pd.DataFrame): train dataset
        test (pd.DataFrame): test dataset
        path (Path): path to save datasets
    Returns:
        None
    """
    train_path = os.path.join(path, "train.csv")
    test_path = os.path.join(path, "test.csv")

    try:
        train.to_csv(train_path)
        logger.info("Train data set successfully saved to %s", path)
    except Exception as e:
        logger.error(
            "Train data set failed to saved to %(p)s due to: %(err)s",
            {"p": path, "err": e},
        )
        raise NotImplementedError from e

    try:
        test.to_csv(test_path)
        logger.info("Test data set successfully saved to %s", path)
    except Exception as e:
        logger.error(
            "Test data set failed to saved to %(p)s due to: %(err)s",
            {"p": path, "err": e},
        )
        raise NotImplementedError from e


def save_model(model: object, path: Path) -> None:
    """save trained model
    Args:
        Args:
        model (object): trained model
        path (Path): path to save model artifacts
    Returns:
        None
    """
    try:
        with open(path, "wb") as file:
            pickle.dump(model, file)
            logger.info("Model binary successfully saved to %s", path)
    except Exception as e:
        logger.error(
            "Model binary failed to save to %(p)s due to: %(err)s",
            {"p": path, "err": e},
        )
        raise NotImplementedError from e
