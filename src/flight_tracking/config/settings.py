import logging
import os
from unittest import case

from dotenv import load_dotenv

load_dotenv()

def get_required_env(key: str) -> str:
    """
    Helper method to get the specified required environment variable from the environment
    :param key: A string containing the required environment variable
    :return: Returns the required environment variable
    """

    value = os.getenv(key)
    if not value:  # Triggers if the variable is missing or empty
        raise ValueError(f"CRITICAL: Missing required environment variable: '{key}'. Please check your .env file.")
    return value

def get_bounding_box() -> tuple:
    """
    Helper method to get a parsed bounding box setting from the environment variable
    :return: Return bounding box setting
    """

    # Fetch the raw string from the environment
    _bbox_str = os.getenv("OPENSKY_API_DEFAULT_BBOX")

    # Parse it into a tuple of floats
    if _bbox_str:
        _bbox_value = tuple(float(coord.strip()) for coord in _bbox_str.split(","))
    else:
        raise ValueError("CRITICAL: Missing required environment variable: 'OPENSKY_API_DEFAULT_BBOX'")

    return _bbox_value

def get_log_level() -> "LoggingLevel":
    """
    Helper method to get the log level
    :return: Returns the log level
    """

    raw_log_level = os.getenv("LOGGING_LEVEL", "INFO")

    match raw_log_level:
        case "INFO":
            return logging.INFO
        case "DEBUG":
            return logging.DEBUG
        case "CRITICAL":
            return logging.CRITICAL
        case "ERROR":
            return logging.ERROR
        case "WARNING":
            return logging.WARNING
        case "NOTSET":
            return logging.NOTSET


class Config:
    """
    Central configuration for the Flight Tracking data pipeline.
    """

    # OpenSky API Credentials
    OPENSKY_USERNAME = get_required_env("OPENSKY_USERNAME")
    OPENSKY_PASSWORD = get_required_env("OPENSKY_PASSWORD")

    # OpenSky API Settings
    OPENSKY_API_URL = os.getenv("OPENSKY_API_URL", "https://opensky-network.org/api")
    OPENSKY_API_BOUNDING_BOX = get_bounding_box()
    OPENSKY_API_REQUEST_TIMEOUT_SECONDS = os.getenv("OPENSKY_API_REQUEST_TIMEOUT_SECONDS", 10)
    OPENSKY_API_MAX_RETRIES = os.getenv("OPENSKY_API_MAX_RETRIES", 5)

    # Logging Settings
    LOGGING_LEVEL = get_log_level()

