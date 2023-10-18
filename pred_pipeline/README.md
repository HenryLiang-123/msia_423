# Clouds

## Overview

This repository contains a modularized data science model pipeline. It is a flexible and extensible framework designed to streamline the process of the machine learning workflow, including data acquisition, feature engineering, model selection, training, evaluation, and deployment. The pipeline is organized into distinct, reusable components that can be easily modified or replaced to meet the specific needs of a wide range of machine learning tasks.

## Table of Contents

- [Clouds](#clouds)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Change directory into repository folder](#2-change-directory-into-repository-folder)
    - [3. Setup AWS credentials for artifact upload to S3](#3-setup-aws-credentials-for-artifact-upload-to-s3)
    - [4. Install required packages (required for local implementation)](#4-install-required-packages-required-for-local-implementation)
  - [Usage](#usage)
    - [1. Local](#1-local)
      - [Pipeline only](#pipeline-only)
      - [Unit Test](#unit-test)
    - [2. Docker](#2-docker)
      - [Pipeline only](#pipeline-only-1)
        - [Build the Docker image](#build-the-docker-image)
        - [Run the entire model pipeline](#run-the-entire-model-pipeline)
      - [Unit Test](#unit-test-1)
        - [Build the Docker image for unit test](#build-the-docker-image-for-unit-test)
        - [Run the tests](#run-the-tests)
  - [Customization](#customization)
    - [Acquire data](#acquire-data)
    - [Create dataset](#create-dataset)
    - [Generate features](#generate-features)
    - [Analysis](#analysis)
    - [Train model](#train-model)
    - [Score model](#score-model)
    - [Evaluate performance](#evaluate-performance)
    - [AWS](#aws)



## Features
- Modularity: The pipeline is designed with independent modules for data processing, feature engineering, model training, evaluation, deployment, and artifact saving.
- Flexibility: Each module can be easily customized to accommodate specific requirements or preferences using [config.yaml](config/config.yaml).
- Compatibility: Supports a wide variety of machine learning models and libraries, including TensorFlow, PyTorch, and scikit-learn. 
- Reproducibility: The entire pipeline and its unit tests can be run inside a docker container.

## Requirements
- Python 3.7 or higher
- See [requirements.txt](requirements.txt).

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MSIA/2023-423-hwl6390-hw2.git
```

### 2. Change directory into repository folder

```bash
cd 2023-423-hwl6390-hw2
```

### 3. Setup AWS credentials for artifact upload to S3

This guide assumes you have installed the `AWS` CLI. If you have not configured an AWS profile, run the following

```bash
aws configure sso --profile my-sso
```
For the purposes of this guide, the name of the AWS profile will be `my-sso`. The user can name it however they like.

After configuring the sso, run the following to login

```bash
aws sso login --profile my-sso
```

After logging in, export the profile as an environment variable

```bash
export AWS_PROFILE=my-sso
```

If you run `aws configure list` and are able to see `my-sso` in the list of profiles, the environment variable has been set correctly.

### 4. Install required packages (required for local implementation)

```bash
pip install -r requirements.txt
```

## Usage

### 1. Local

#### Pipeline only

Verify you are in the same directory as `pipeline.py`. Then, run

```bash
python pipeline.py
```
in the terminal.

#### Unit Test

Run

```bash
pytest
```
in the terminal

### 2. Docker

#### Pipeline only

##### Build the Docker image

```bash
docker build -t pipeline -f dockerfiles/dockerfile-pipeline .
```

##### Run the entire model pipeline

```bash
docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=my-sso pipeline
```

#### Unit Test

##### Build the Docker image for unit test

```bash
docker build -t unittest-pipeline -f dockerfiles/dockerfile-test .
```

##### Run the tests

```bash
docker run unittest-pipeline
```

## Customization

To customize settings within the pipeline, edit [config.yaml](config/config.yaml).

### Acquire data

Modify `run_config` section in `config.yaml` to achieve desired dataset and output locations.

### Create dataset

Modify `create_dataset` section in `config.yaml` to achieve desired dataset characteristics and output locations.

### Generate features

Modify `generate_features` section in `config.yaml` to achieve desired features and operations to achieve those features.

### Analysis

Modify `mpl_config` and `eda` sections in `config.yaml` to adjust matplotlib settings, create desired visualizations. Set desired save locations using `figure_dir` in `run_config` section of `config.yaml`.

### Train model

Modify `train_model` section of `config.yaml` to adjust train test split, features, model configuration, hyperparameters, and directory to save model artifacts.

### Score model

Modify `score_model` section of `config.yaml` to adjust settings for model output.

### Evaluate performance

Modify `evaluate_performance` section of `config.yaml` to adjust metrics used for evaluating model performance.

### AWS

Modify `aws` section of `config.yaml` to achieve desired bucket name and prefixes.

