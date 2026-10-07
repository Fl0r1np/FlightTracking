import logging
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError
from opensky_api import TokenManager

from flight_tracking.config.settings import Config
from flight_tracking.ingestion.storage import storage
from flight_tracking.models.bbox import BoundingBox

logger = logging.getLogger(__name__)

class OpenSkyExtractor:
    def __init__(self, token_manager: TokenManager = None):
        self.token_manager = token_manager
        self.session = requests.Session()
        self.base_url = Config.OPENSKY_API_URL.rstrip('/')
        self.default_bbox = BoundingBox.from_tuple(Config.OPENSKY_API_BOUNDING_BOX)
        self.timeout = float(Config.OPENSKY_API_REQUEST_TIMEOUT_SECONDS)

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

            # Handle 429 Too Many Requests explicitly
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "unknown")
                logger.warning(f"Rate limit exceeded (429 Too Many Requests). Retry-After: {retry_after} seconds.")
            # Handle 5xx server errors explicitly
            elif 500 <= response.status_code < 600:
                logger.warning(f"Transient server error encountered. Status Code: {response.status_code}.")

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