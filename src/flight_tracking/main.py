import logging
import flight_tracking.config.logger
from opensky_api import TokenManager
from config.settings import Config
from flight_tracking.ingestion.extractor import OpenSkyExtractor
from flight_tracking.ingestion.alerting import send_alert

if __name__ == '__main__':

    logger = logging.getLogger(__name__)

    logger.info('OpenSky Flight Tracking Ingestion starting...')

    # Load OpenSky API Credentials
    opensky_username = Config.OPENSKY_USERNAME
    opensky_password = Config.OPENSKY_PASSWORD
    opensky_api_url = Config.OPENSKY_API_URL
    opensky_api_bounding_box = Config.OPENSKY_API_BOUNDING_BOX
    opensky_api_request_timeout = Config.OPENSKY_API_REQUEST_TIMEOUT_SECONDS
    opensky_api_max_retries = Config.OPENSKY_API_MAX_RETRIES

    #print(f"OpenSky Information: {opensky_username}:{opensky_password}, {opensky_api_url}, {opensky_api_bounding_box}, {opensky_api_request_timeout}, {opensky_api_max_retries}")
    #token_manager = TokenManager(opensky_username, opensky_password)
    #api = OpenSkyExtractor(token_manager)
    #print(api.fetch_flight_states())

    # Test Slack alerting
    send_alert(" *[FlightTracking Pipeline]* Extraction failed after 5 retries.\n*Error Type:* Timeout\n*Message:* Connection lost.")

    logger.info('OpenSky Flight Tracking Ingestion finishing...')



