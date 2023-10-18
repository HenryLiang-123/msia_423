import os
import logging
from typing import List
from pathlib import Path
import boto3

logger = logging.getLogger("clouds")


def check_bucket_exists(bucket_name: str, s3_client) -> None:
    """Check if s3 bucket exists
    Args:
        bucket_name (str): name of bucket to check
        config (dict): configuration for s3 bucket
        s3_client: s3 client in use
    Return:
        None
    """
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(
            "Bucket %s exists. Writing directly to the specified bucket", bucket_name
        )
    except Exception as e_1:
        try:
            error_code = int(e_1.response["Error"]["Code"])
            if error_code == 404:
                logger.error(
                    "Bucket %s does not exist. Please create it prior to running the application.",
                    bucket_name,
                )
        except AttributeError:
            logger.error(
                "Bucket %(bucket_name)s failed to be found due to %(error)s ",
                {"bucket_name": bucket_name, "error": e_1},
            )
        except Exception as e_2:
            logger.error(
                "Failed to find bucket %(bucket_name)s due to %(error)s",
                {"bucket_name": bucket_name, "error": e_1},
            )
            raise NotImplementedError from e_2


def upload_artifacts(artifacts: Path, config: dict) -> List[str]:
    """Upload model artifacts to specified S3 bucket
    Args:
        artifacts (Path): Path to artifacts
        config (dict): Configuration of s3 bucket
    Return:
        None
    """
    s_3 = boto3.client("s3")
    bucket_name = config["bucket_name"]
    prefix = config["prefix"]

    check_bucket_exists(bucket_name, s_3)

    s3_uris = []

    for root, _, files in os.walk(artifacts):
        for file in files:
            local_file_path = os.path.join(root, file)

            s3_key = os.path.relpath(local_file_path, artifacts).replace("\\", "/")
            s3_key_final = Path(prefix + "/" + s3_key)

            with open(local_file_path, "rb") as file_data:
                try:
                    s_3.put_object(
                        Bucket=bucket_name, Key=str(s3_key_final), Body=file_data
                    )
                    logger.info(
                        "Uploaded %(lfp)s to S3 location:  %(bucket_name)s/%(prefix)s/%(s3_key)s",
                        {
                            "lfp": local_file_path,
                            "bucket_name": bucket_name,
                            "prefix": prefix,
                            "s3_key": s3_key,
                        },
                    )
                except Exception as e:
                    logger.error(
                        "Failed to upload %(lfp)s to S3 location: %(bucket_name)s/%(prefix)s/%(s3_key)s",
                        {
                            "lfp": local_file_path,
                            "bucket_name": bucket_name,
                            "prefix": prefix,
                            "s3_key": s3_key,
                        },
                    )
                    raise NotImplementedError from e

            s3_uris.append(f"s3://{bucket_name}/{prefix}/{s3_key}")

    return s3_uris
