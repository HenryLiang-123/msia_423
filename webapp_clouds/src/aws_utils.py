"""
This module provides utility functions to interact with AWS S3 service, specifically
for downloading files to local storage. It also includes configurations for logging.
The module is primarily designed for use with the Streamlit framework, providing
caching functionality to optimize performance.

Functions:
    download_s3: This function fetches and downloads a specified file from an S3
    bucket to a local path. It uses the Boto3 client to interact with AWS S3.
    The downloaded file path is returned. The function is also decorated with a
    Streamlit caching function to prevent redundant download operations and improve performance.
"""

import logging
from pathlib import Path
import boto3
import streamlit as st

logger = logging.getLogger("clouds")

@st.cache_resource
def download_s3(bucket_name: str, object_key: str, local_file_path: Path) -> None:
    """
    Download a file from an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key of the object in the S3 bucket.
        local_file_path (Path): The local path where the file will be downloaded.

    Returns:
        None
    """
    s3_client = boto3.client("s3")
    print(f"Fetching Key: {object_key} from S3 Bucket: {bucket_name}")
    try:
        s3_client.download_file(bucket_name, object_key, str(local_file_path))
        logger.info("Model files successfully downloaded to local")
    except Exception as e_1:
        logger.error("Failed to download model files due to %(error)s", {"error": e_1})
        raise NotImplementedError from e_1
