from opensky_api import OpenSkyApi, TokenManager

from flight_tracking.config.settings import Config
from flight_tracking.models.bbox import BoundingBox


class OpenSkyAPIFacade:

    DEFAULT_BOUNDING_BOX = Config.OPENSKY_API_BOUNDING_BOX

    def __init__(self, client_id: str, client_secret: str):
        self.api_client = OpenSkyApi(TokenManager(client_id, client_secret))

    def fetch_flight_states(self, _bbox=BoundingBox.from_tuple(DEFAULT_BOUNDING_BOX)):
        """
        A method to fetch flight states from OpenSky API
        :param _bbox: A BoundingBox object representing the bounding box
        :return: Returns a list of flight states
        """
        response = self.api_client.get_states(bbox=_bbox.get_value())
        return response