from config.settings import Config
from flight_tracking.ingestion.extractor import OpenSkyAPIFacade
from flight_tracking.config.logger import logger

if __name__ == '__main__':

    logger.info('OpenSky Flight Tracking Ingestion starting...')

    # Load OpenSky API Credentials
    opensky_username = Config.OPENSKY_USERNAME
    opensky_password = Config.OPENSKY_PASSWORD
    opensky_api_url = Config.OPENSKY_API_URL
    opensky_api_bounding_box = Config.OPENSKY_API_BOUNDING_BOX
    opensky_api_request_timeout = Config.OPENSKY_API_REQUEST_TIMEOUT_SECONDS
    opensky_api_max_retries = Config.OPENSKY_API_MAX_RETRIES

    #print(f"OpenSky Information: {opensky_username}:{opensky_password}, {opensky_api_url}, {opensky_api_bounding_box}, {opensky_api_request_timeout}, {opensky_api_max_retries}")
    logger.info('Fetch current flight states with the default bbox')
    api = OpenSkyAPIFacade(opensky_username, opensky_password)
    print(api.fetch_flight_states())
    logger.info('Fetch current flight states executed successfully')

    logger.info('OpenSky Flight Tracking Ingestion finishing...')



