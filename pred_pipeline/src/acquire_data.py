import logging
import sys
import time
from pathlib import Path

import requests

logger = logging.getLogger("clouds")


def get_data(
    url: str, attempts: int = 4, wait: int = 3, wait_multiple: int = 2
) -> bytes:
    """Acquires data from URL
    Args:
        Args:
        url (str): The URL to fetch the data from.
        attempts (int, optional): The number of retry attempts. Defaults to 4.
        wait (int, optional): The initial wait time between attempts in seconds. Defaults to 3.
        wait_multiple (int, optional): The multiplier for the wait time for each subsequent attempt. Defaults to 2.

    Returns:
        Optional[bytes]: The fetched data as bytes if successful, otherwise None.
    """

    for attempt in range(attempts):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
            return response.content
        except requests.exceptions.RequestException as e:
            logger.warning(
                "Error on attempt %(attempt_number)s: %(error_message)s",
                 {"attempt_number": attempt + 1, "error_message": e}
            )
            if attempt < attempts - 1:
                wait_time = wait * (wait_multiple**attempt)
                logger.warning("Waiting for %s seconds before retrying...", wait_time)
                time.sleep(wait_time)
            else:
                logger.error("All attempts failed.")
                raise NotImplementedError


def write_data(data: bytes, save_path: Path) -> None:
    """Writes data to a file at the specified path.

    Args:
        data (bytes): The data to be written to the file.
        save_path (Path): The local path to save the data.
    """
    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True)
    try:
        with save_path.open("wb") as f:
            f.write(data)
    except Exception as e:
        logger.error("Failed to write data to %s", save_path)
        raise NotImplementedError from e



def acquire_data(url: str, save_path: Path) -> None:
    """Acquires data from specified URL

    Args:
        url: URL for where data to be acquired is stored
        save_path: Local path to write data to
    """
    url_contents = get_data(url)
    try:
        write_data(url_contents, save_path)
        logger.info("Data written to %s", save_path)
    except FileNotFoundError:
        logger.error("Please provide a valid file location to save dataset to.")
        sys.exit(1)
    except Exception as e:
        logger.error("Error occurred while trying to write dataset to file: %s", e)
        sys.exit(1)
