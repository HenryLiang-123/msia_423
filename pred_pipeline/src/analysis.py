import logging
import os
from typing import List
from pathlib import Path
from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

logger = logging.getLogger("clouds")
def save_figures(data: pd.DataFrame, fig_dir: Path, config: dict) -> List[Path]:
    """Create and save eda figures

    Args:
        data (pd.DataFrame): data with generated features and response
        fig_dir (Path): Path to save eda figures
        stat_dir (Path): Path to save stats
        config (dict): configuration

    Returns:
        None
    """

    # Config for matplotlib
    mpl_config = config["mpl_config"]
    mpl_update = {
        "font.size": mpl_config["font.size"],
        "axes.prop_cycle": cycler(
            mpl_config["axes.prop_cycle"], mpl_config["axes.prop_cycle_colors"]
        ),
        "xtick.labelsize": mpl_config["xtick.labelsize"],
        "ytick.labelsize": mpl_config["ytick.labelsize"],
        "figure.figsize": mpl_config["figure.figsize"],
        "axes.labelsize": mpl_config["axes.labelsize"],
        "axes.labelcolor": mpl_config["axes.labelcolor"],
        "axes.titlesize": mpl_config["axes.titlesize"],
        "lines.color": mpl_config["lines.color"],
        "lines.linewidth": mpl_config["lines.linewidth"],
        "text.color": mpl_config["text.color"],
        "font.family": mpl_config["font.family"],
        "font.sans-serif": mpl_config["font.sans-serif"],
    }
    mpl.rcParams.update(mpl_update)

    # Data
    data_config = config["generate_features"]
    target = data[data_config["target_col"]]
    features = data[data_config["feature_col"]]
    figs = []
    eda_fig_config = config["eda"]["fig_config"]
    for feat in features.columns:
        fig, ax = plt.subplots(
            figsize=(eda_fig_config["figsize_x"], eda_fig_config["figsize_y"])
        )
        ax.hist(
            [features[target == 0][feat].values, features[target == 1][feat].values]
        )
        ax.set_xlabel(" ".join(feat.split("_")).capitalize())
        ax.set_ylabel("Number of observations")

        # Save fig
        fig_name = f"{feat}_eda_plot.png"
        fig_path = os.path.join(fig_dir, fig_name)
        try:
            fig.savefig(fig_path, bbox_inches="tight")
            logger.info("%(fname)s saved to %(fpath)s", {"fname":fig_name, "fpath": fig_path})
        except Exception as e:
            logger.error("Failed to save %(fname)s to %(fpath)s", {"fname":fig_name, "fpath": fig_path})
            raise NotImplementedError from e
        figs.append(fig)
