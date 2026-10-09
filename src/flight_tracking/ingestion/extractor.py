import logging
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
from opensky_api import TokenManager
from flight_tracking.config.settings import Config
from flight_tracking.ingestion.storage import storage
from flight_tracking.models.bbox import BoundingBox
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from flight_tracking.utils.retry_utils import is_transient_error, log_retry_attempt

logger = logging.getLogger(__name__)

class OpenSkyExtractor:
    def __init__(self, token_manager: TokenManager = None):
        self.token_manager = token_manager
        self.session = requests.Session()
        self.base_url = Config.OPENSKY_API_URL.rstrip('/')
        self.default_bbox = BoundingBox.from_tuple(Config.OPENSKY_API_BOUNDING_BOX)
        self.timeout = float(Config.OPENSKY_API_REQUEST_TIMEOUT_SECONDS)

    @retry(
        wait=wait_exponential(multiplier=2, min=2, max=16), # Wait 2s, 4s, 8s, 16s
        stop=stop_after_attempt(int(Config.OPENSKY_API_MAX_RETRIES)),
        retry=retry_if_exception(is_transient_error), # Point to the custom evaluation function
        before_sleep=log_retry_attempt,
        reraise=True
    )
    def fetch_flight_states(self, bbox: BoundingBox = None):
        """
        A method to fetch flight states from OpenSky API
        :param bbox: A BoundingBox object representing the bounding box.
        :return: Returns a dict of the raw JSON response.
        """

        logger.info(f"Starting to fetch flight states from OpenSky API.")

        if bbox is None:
            bbox = self.default_bbox

        headers = {}
        if self.token_manager:
            try:
                headers.update(self.token_manager.auth_headers())
            except Exception as e:
                logger.debug(f"Could not retrieve auth headers: {e}")

        params = {
            "lamin": bbox.lamin,
            "lomin": bbox.lomin,
            "lamax": bbox.lamax,
            "lomax": bbox.lomax,
        }

        endpoint = f"{self.base_url}/states/all"

        try:
            response = self.session.get(
                endpoint,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            # Raise HTTPError for any non-2xx response
            response.raise_for_status()

            # Save the raw data to storage
            raw_json = response.json()
            storage.save_raw_data(raw_json)

            logger.info("Successfully fetched flight states from OpenSky API.")
            return raw_json

        except Timeout as e:
            logger.error(f"Request to OpenSky API timed out: {e}")
            raise
        except ConnectionError as e:
            logger.error(f"Connectivity error occurred while reaching OpenSky API: {e}")
            raise
        except HTTPError as e:
            logger.error(f"HTTP Error occurred: {e}")
            raise