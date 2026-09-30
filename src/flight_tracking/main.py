import os
from config.settings import Config

if __name__ == '__main__':

    # Load OpenSky API Credentials
    opensky_username = Config.OPENSKY_USERNAME
    opensky_password = Config.OPENSKY_PASSWORD
    opensky_api_url = Config.OPENSKY_API_URL
    opensky_api_bounding_box = Config.OPENSKY_API_BOUNDING_BOX
    opensky_api_request_timeout = Config.OPENSKY_API_REQUEST_TIMEOUT_SECONDS
    opensky_api_max_retries = Config.OPENSKY_API_MAX_RETRIES

    print(f"OpenSky Information: {opensky_username}:{opensky_password}, {opensky_api_url}, {opensky_api_bounding_box}, {opensky_api_request_timeout}, {opensky_api_max_retries}")