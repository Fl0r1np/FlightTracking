from opensky_api import OpenSkyApi, TokenManager

class OpenSkyAPIFacade:

    def __init__(self, client_id: str, client_secret: str):
        self.api_client = OpenSkyApi(TokenManager(client_id, client_secret))

    def get_states(self, _bbox):
        response = self.api_client.get_states(bbox=_bbox)
        return response