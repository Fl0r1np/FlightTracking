from requests.exceptions import Timeout, HTTPError
import logging
from tenacity import retry, RetryCallState

from flight_tracking.config.settings import Config

logger = logging.getLogger(__name__)

def is_transient_error(exception: Exception) -> bool:
    """
    Verifies if the given exception is a transient error or not.
    :param exception: The exception to verify.
    :return: True if the exception is a transient error, false otherwise.
    """
    if isinstance(exception, (Timeout, ConnectionError)):
        return True
    if isinstance(exception, HTTPError) and (exception.response.status_code == 429 or exception.response.status_code >= 500):
        return True
    return False

def log_retry_attempt(retry_state: RetryCallState) -> None:
    """
    Logs a retry attempt.
    :param retry_state: A retry state object from tenacity
    :return: Nothing
    """
    max_retries = Config.OPENSKY_API_MAX_RETRIES
    exception = retry_state.outcome.exception()
    logger.warning(f"Retry {retry_state.attempt_number}/{max_retries}: API returned {type(exception).__name__} ({exception}), waiting {retry_state.next_action.sleep} seconds...")
    pass