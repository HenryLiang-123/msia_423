from pathlib import Path
from importlib import import_module
import logging
import yaml
import pandas as pd
import numpy as np

logger = logging.getLogger("clouds")


def numpy_to_native(obj):
    """
    Numpy to native types
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


def evaluate_performance(
    test: pd.DataFrame, scores: pd.DataFrame, config: dict
) -> dict:
    """Calculate performance metrics of model
    Args:
        Args:
        test (pd.DataFrame): test dataset
        scores (pd.DataFrame): dataframe of the model output (probability and class)
        config (dict): configurations for model performance metrics
    Returns:
        metric_dict (dict): dictionary with key value pairs as metric-value.
    """
    y_test = test[config["target"]]
    metrics_lib = import_module(config["metrics_lib"])
    metric_dict = {}
    for metric in config["metrics"]:
        metric_type = getattr(metrics_lib, metric)
        if metric == "roc_auc_score":
            value = metric_type(y_test, scores[0])
        else:
            value = metric_type(y_test, scores[1])
        metric_dict[metric] = numpy_to_native(value)

    logger.info("Dic with metrics created")
    return metric_dict


def save_metrics(metrics: dict, path: Path) -> None:
    """Save values of model performance metrics
    Args:
        Args:
        metrics (dict): dictionary of metrics
        path (Path): path to save metrics
    Returns:
        None
    """
    try:
        with open(path, "w") as file:
            yaml.dump(metrics, file)
            logger.info("Metrics yaml file created at %s", path)
    except Exception as e:
        logger.warning("Failed to save metrics yaml file to %s", path)
        raise NotImplementedError from e
