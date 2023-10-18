# Clouds

## Table of Contents

- [Clouds](#clouds)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Change directory into repository folder](#2-change-directory-into-repository-folder)
    - [3. Setup AWS credentials for artifact download from S3](#3-setup-aws-credentials-for-artifact-download-from-s3)
    - [4. Install required packages (required for local implementation)](#4-install-required-packages-required-for-local-implementation)
  - [Usage](#usage)
    - [1. Local](#1-local)
      - [Pipeline only](#pipeline-only)
      - [Unit Test](#unit-test)
    - [2. Docker](#2-docker)
      - [Pipeline only](#pipeline-only-1)
        - [Build the Docker image](#build-the-docker-image)
        - [Run the application](#run-the-application)
      - [Unit Test](#unit-test-1)
        - [Build the Docker image for unit test](#build-the-docker-image-for-unit-test)
        - [Run the tests](#run-the-tests)
  - [Customization](#customization)
    - [AWS](#aws)


## Overview

This repository contains the Clouds project, an interactive web application built with Streamlit, which allows users to select and run different versions of trained machine learning models. This document includes a guide for setting up, installing, retrieving models, setting up the Streamlit application, usage, customization, and troubleshooting.

## Features

The main feature of this project is the Streamlit-based web application, which allows users to load, select and run different versions of trained machine learning models. The application also includes a comprehensive testing framework, logging and error handling mechanisms to ensure a smooth and robust user experience. Each module can be easily customized to accommodate specific requirements or preferences using [config.yaml](config/config.yaml). The entire application and its unit tests can be run inside a docker container. The application has also been deployed on AWS ECS, but has been stopped mainly for cost reasons.

## Requirements
- Python 3.7 or higher
- Streamlit
- Docker
- AWS credentials
- See [requirements.txt](requirements.txt).
- The application assumes that an S3 bucket with trained model objects and training data has already been setup. It will *not* set one up for you.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MSIA/423-2023-hw3-hwl6390.git
```

### 2. Change directory into repository folder

```bash
cd 423-2023-hw3-hwl6390
```

### 3. Setup AWS credentials for artifact download from S3

This guide assumes you have installed the `AWS` CLI. If you have not configured an AWS profile, run the following.

```bash
aws configure sso --profile my-sso
```
For the purposes of this guide, the name of the AWS profile will be `my-sso`. The user can name it however they like.

After configuring the sso, run the following to login.

```bash
aws sso login --profile my-sso
```

After logging in, export the profile as an environment variable.

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

Verify you are in the same directory as `main.py`. Then, run

```bash
streamlit run main.py
```
in the terminal.

#### Unit Test

Run

```bash
pytest
```
in the terminal.

### 2. Docker

#### Pipeline only

##### Build the Docker image

```bash
docker build -t clouds-app -f dockerfiles/docker-main .
```

##### Run the application

```bash
docker run -p 80:80 -v ~/.aws:/root/.aws -e AWS_PROFILE=my-sso clouds-app
```

#### Unit Test

##### Build the Docker image for unit test

```bash
docker build -t unittest-cloud -f dockerfiles/docker-test .
```

##### Run the tests

```bash
docker run unittest-cloud
```

## Customization

To customize settings within the pipeline, edit [config.yaml](config/config.yaml).

### AWS

Modify `aws` section of `config.yaml` to achieve desired bucket name and prefixes.
