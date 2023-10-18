import logging
from pathlib import Path
import pandas as pd
import numpy as np

logger = logging.getLogger("clouds")


def create_dataset(path_of_raw: Path, config: dict) -> pd.DataFrame:
    """Create pandas dataframe from path
    Args:
        Args:
        path_of_raw (Path): the path where raw data is
        config (dict): config file for dataset creation

    Returns:
        pd.Dataframe: clean dataset
    """
    # Dataset column names
    columns = config["data"]["columns"]
    with open(path_of_raw, "r") as f:
        data = [[s for s in line.split(" ") if s != ""] for line in f.readlines()]

    # Select first cloud
    first_cloud_data_left = config["data_prep"]["first_cloud"]["left"]
    first_cloud_data_right = config["data_prep"]["first_cloud"]["right"]

    if len(data[first_cloud_data_left]) != len(columns):
        logger.warning(
            "The %sth row of the first dataset does not have the same number of values as the columns",
            first_cloud_data_left,
        )

    if len(data[first_cloud_data_right - 1]) != len(columns):
        logger.warning(
            "The %sth row of the first dataset does not have the same number of values as the columns",
            first_cloud_data_right,
        )

    first_cloud = data[first_cloud_data_left:first_cloud_data_right]
    try:
        first_cloud = [
            [float(s.replace("/n", "")) for s in cloud] for cloud in first_cloud
        ]
    except ValueError as e:
        logger.error(e)
        raise NotImplementedError from e

    first_cloud = pd.DataFrame(first_cloud, columns=columns)
    first_cloud["class"] = np.zeros(len(first_cloud))

    # Select second cloud
    second_cloud_data_left = config["data_prep"]["second_cloud"]["left"]
    second_cloud_data_right = config["data_prep"]["second_cloud"]["right"]

    if len(data[second_cloud_data_left]) != len(columns):
        logger.warning(
            "The %sth row of the second dataset does not have the same number of values as the columns",
            second_cloud_data_left,
        )

    if len(data[second_cloud_data_right - 1]) != len(columns):
        logger.warning(
            "The %sth row of the second dataset does not have the same number of values as the columns",
            second_cloud_data_right,
        )

    second_cloud = data[second_cloud_data_left:second_cloud_data_right]
    try:
        second_cloud = [
            [float(s.replace("/n", "")) for s in cloud] for cloud in second_cloud
        ]
    except ValueError as e:
        logger.error(e)
        raise NotImplementedError from e
    second_cloud = pd.DataFrame(second_cloud, columns=columns)
    second_cloud["class"] = np.ones(len(second_cloud))

    # Create final
    data = pd.concat([first_cloud, second_cloud])

    logger.info("Clean dataset created")

    return data


def save_dataset(data: pd.DataFrame, path_of_clean: Path) -> None:
    """Save dataframe to csv in path
    Args:
        Args:
        data (pd.Dataframe): pandas dataframe to save
        path_of_clean (Path): paht to save cleaned dataset

    Returns:
        None
    """
    try:
        data.to_csv(path_of_clean)
        logger.info("Saved dataset to %s", path_of_clean)
    except Exception as e:
        logger.error("Failed to save dataset due to: %s", e)
        raise NotImplementedError from e
