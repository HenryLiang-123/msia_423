import argparse
import datetime
import logging.config
from pathlib import Path
import yaml
import src.acquire_data as ad
import src.analysis as eda
import src.aws_utils as aws
import src.create_dataset as cd
import src.evaluate_performance as ep
import src.generate_features as gf
import src.score_model as sm
import src.train_model as tm

logging.config.fileConfig("config/logging/local.conf", disable_existing_loggers=True)
logger = logging.getLogger("clouds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Acquire, clean, and create features from clouds data"
    )
    parser.add_argument(
        "--config", default="config/config.yaml", help="Path to configuration file"
    )
    args = parser.parse_args()

    # Load configuration file for parameters and run config
    with open(args.config, "r") as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.error.YAMLError as e:
            logger.error("Error while loading configuration from %s", args.config)
        else:
            logger.info("Configuration file loaded from %s", args.config)

    run_config = config.get("run_config", {})
    # Set up output directory for saving artifacts
    now = int(datetime.datetime.now().timestamp())
    artifacts = Path(run_config["output"]["runs"]) / str(now)
    artifacts.mkdir(parents=True)

    # Create separate directories for raw and processed data
    raw_data_dir = artifacts / Path(run_config["data_dir"]["raw"])
    processed_data_dir = artifacts / Path(run_config["data_dir"]["processed"])
    raw_data_dir.mkdir(parents=True)
    processed_data_dir.mkdir(parents=True)

    # Save config file to artifacts directory for traceability
    with (artifacts / "config.yaml").open("w") as f:
        yaml.dump(config, f)

    # Acquire data from online repository and save to disk
    ad.acquire_data(run_config["data_source"], raw_data_dir / "clouds.data")

    # Create structured dataset from raw data; save to disk
    data = cd.create_dataset(raw_data_dir / "clouds.data", config["create_dataset"])
    cd.save_dataset(data, processed_data_dir / "clouds.csv")

    # Enrich dataset with features for model training; save to disk
    features = gf.generate_features(data, config["generate_features"])

    # Generate statistics and visualizations for summarizing the data; save to disk
    figures = artifacts / Path(run_config["figure_dir"])
    figures.mkdir()
    eda.save_figures(features, figures, config)

    # Split data into train/test set and train model based on config; save each to disk
    tmo, train, test = tm.train_model(features, config["train_model"])
    model_data_dir = artifacts / Path(config["train_model"]["data_dir"])
    model_data_dir.mkdir(parents=True)
    tm.save_data(train, test, model_data_dir)

    model_dir = artifacts / Path(config["train_model"]["model_dir"])
    model_dir.mkdir(parents=True)
    tm.save_model(tmo, model_dir / "trained_model_object.pkl")

    # Score model on test set; save scores to disk
    scores = sm.score_model(test, tmo, config["score_model"])
    score_dir = artifacts / Path(config["score_model"]["score_dir"])
    score_dir.mkdir(parents=True)
    sm.save_scores(scores, score_dir / "scores.csv")

    # Evaluate model performance metrics; save metrics to disk
    metrics = ep.evaluate_performance(test, scores, config["evaluate_performance"])
    metric_dir = artifacts / Path(config["evaluate_performance"]["metric_dir"])
    metric_dir.mkdir(parents=True)
    ep.save_metrics(metrics, metric_dir / "metrics.yaml")

    # Upload all artifacts from all runs to S3
    # Partitioned folders by timestamp in S3
    aws_config = config.get("aws")
    all_artifacts = Path(run_config["output"]["runs"])
    if aws_config.get("upload"):
        aws.upload_artifacts(all_artifacts, aws_config)
