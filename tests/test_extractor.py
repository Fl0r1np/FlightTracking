import pytest
import responses
from unittest.mock import patch
from requests.exceptions import HTTPError, Timeout

from flight_tracking.config.settings import Config
from flight_tracking.ingestion.extractor import OpenSkyExtractor

# Settings
API_BASE_URL = Config.OPENSKY_API_URL
FETCH_FLIGHT_STATES_URL = f"{API_BASE_URL}/states/all"
API_MAX_RETRIES = Config.OPENSKY_API_MAX_RETRIES

@pytest.fixture(autouse=True)
def bypass_sleep():
    """Forces tenacity to skip waiting during retries for blazing fast tests."""
    with patch('time.sleep', return_value=None):
        yield

@responses.activate
def test_successful_fetch_flight_states():
    # Mock request
    json_response = {
            "time": 10,
            "states": [
                [1,2],
                [3,4]
            ]
        }
    responses.add(
        responses.GET,
        FETCH_FLIGHT_STATES_URL,
        json=json_response,
        status=200
    )
    # Mock api call
    extractor = OpenSkyExtractor()
    result = extractor.fetch_flight_states()
    assert result == json_response
    assert len(responses.calls) == 1

@responses.activate
def test_429_triggers_retry_and_fails():
    # Mock request
    responses.add(
        responses.GET,
        FETCH_FLIGHT_STATES_URL,
        json={
            "error":"Rate limit exceeded"
        },
        status=429
    )
    # Mock api call
    extractor = OpenSkyExtractor()
    with pytest.raises(HTTPError) as exc_info:
        extractor.fetch_flight_states()
    assert exc_info.value.response.status_code == 429
    assert len(responses.calls) == API_MAX_RETRIES

@responses.activate
def test_500_internal_server_error():
    # Mock request
    responses.add(
        responses.GET,
        FETCH_FLIGHT_STATES_URL,
        json={
            "error": "Internal Server Error"
        },
        status=500
    )
    # Mock api call
    extractor = OpenSkyExtractor()
    with pytest.raises(HTTPError) as exc_info:
        extractor.fetch_flight_states()
    assert exc_info.value.response.status_code == 500
    assert len(responses.calls) == API_MAX_RETRIES

@responses.activate
def test_timeout_triggers_retry():
    # Mock request
    responses.add(
        responses.GET,
        FETCH_FLIGHT_STATES_URL,
        body=Timeout("Connection timed out!")
    )
    # Mock api call
    extractor = OpenSkyExtractor()
    with pytest.raises(Timeout):
        extractor.fetch_flight_states()
    assert len(responses.calls) == API_MAX_RETRIES