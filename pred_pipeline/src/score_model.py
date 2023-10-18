from pathlib import Path
from typing import Tuple
import logging
import pandas as pd

logger = logging.getLogger("clouds")


def score_model(test: pd.DataFrame, model: object, config: dict) -> Tuple[list, list]:
    """score saved model
    Args:
        Args:
        test (pd.DataFrame): test dataset
        model (object): model to score
        config (dict): configurations for scoring the model
    Returns:
        ypred_proba_test (list): predicted probabilities of positve class
        ypred_bin_test (list): predicted classes
    """
    initial_features = config["initial_features"]
    x_test = test[initial_features]

    ypred_proba_test = model.predict_proba(x_test)[:, 1]
    ypred_bin_test = model.predict(x_test)
    logger.info("Model predictions (probability and class) created")

    return (ypred_proba_test, ypred_bin_test)


def save_scores(scores: tuple, path: Path) -> None:
    """save output of the model
    Args:
        Args:
        scores (tuple(list, list)): predicted scores of model
        path (Path): path to save model outputs
    Returns:
        None
    """
    pred_prob = scores[0]
    pred_class = scores[1]
    out = pd.DataFrame({"Probability": pred_prob, "Class": pred_class})
    try:
        out.to_csv(path)
        logger.info("Model predictions saved to %s", path)
    except Exception as e:
        logger.error(
            "Model predictions failed to save to %(p)s due to %(err)s",
            {"p": path, "err": e},
        )
        raise NotImplementedError from e
