import os
from dotenv import load_dotenv

# We call load_dotenv() here so that any file importing this config
# will automatically have the environment variables loaded.
load_dotenv()

class Config:
    """Central configuration for the Flight Tracking data pipeline."""

    # OpenSky API Credentials
    OPENSKY_USERNAME = os.getenv("OPENSKY_USERNAME")
    OPENSKY_PASSWORD = os.getenv("OPENSKY_PASSWORD")

    # OpenSky API Settings
    OPENSKY_API_URL = os.getenv("OPENSKY_API_URL", "https://opensky-network.org/api")
    OPENSKY_API_BOUNDING_BOX = os.getenv("OPENSKY_API_BOUNDING_BOX")
    OPENSKY_API_REQUEST_TIMEOUT_SECONDS = os.getenv("OPENSKY_API_REQUEST_TIMEOUT_SECONDS")
    OPENSKY_API_MAX_RETRIES = os.getenv("OPENSKY_API_MAX_RETRIES")

