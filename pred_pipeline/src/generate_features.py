import logging
import pandas as pd
import numpy as np

logger = logging.getLogger("clouds")


def recursive_operation(operation: dict, features: pd.DataFrame) -> pd.Series:
    """Create features
    Args:
        operation (dict): dictionary of operations to complete
        features (pd.DataFrame): feature dataframe to augment

    Returns:
        pd.Series: series with complete operation values
    """
    if isinstance(operation, str):
        return features[operation]
    curr_op = operation["operation"]
    try:
        source1 = recursive_operation(operation["source1"], features)
        source2 = recursive_operation(operation["source2"], features)
    except KeyError:
        source1 = recursive_operation(operation["source1"], features)

    if curr_op == "apply":
        function = getattr(np, operation["function"])
        return source1.apply(function)
    elif curr_op == "multiply":
        return source1.multiply(source2)
    elif curr_op == "subtract":
        return source1.subtract(source2)
    elif curr_op == "divide":
        return source1.divide(source2)
    elif curr_op == "add":
        return source1.add(source2)
    else:
        logger.error("Invalid operation %s supplied.", curr_op)
        raise NotImplementedError


def generate_features(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Create features
    Args:
        data (pd.Dataframe): original, clean, unmodified dataset
        config (dict): feature engineering configs

    Returns:
        pd.Dataframe: dataframe with additional engineered features
    """

    columns = config["feature_col"]
    response = config["target_col"]
    features = data[columns]
    features[config["target_col"]] = data[response]

    try:
        for operation in config["feature_eng"]:
            target = operation["target"]
            features[target] = recursive_operation(operation, features)
            logger.info("Feature %s created.", target)
    except Exception as e:
        logger.error(
            "Feature %(t)s could not be created due to %(err)s Please check the formatting of config.yaml",
            {"t": target, "err": e},
        )
        raise e

    return features
