import logging
import requests
from requests.exceptions import RequestException

from flight_tracking.config.settings import Config


logger = logging.getLogger(__name__)


def send_alert(message:str):
    """
    A method to send an alert message to a webhook url
    :param message: A string representing the alert message to be sent
    :return: Nothing
    """

    logger.info("Trying to send an alert message to slack webhook!")

    # If there is no webhook set, skip
    webhook = Config.ALERT_WEBHOOK_URL
    if webhook is None:
        logger.warning("Slack webhook is not set. Skipping alert!")
        return

    # Try to send the alert message
    payload = {
        "text": message,
    }
    try:
        response = requests.post(webhook, json=payload, timeout=5)
        response.raise_for_status()
        logger.info(f"Successfully sent alert message to slack webhook!")
    except RequestException as e:
        logger.error(f"Failed to send Slack alert. Webhook unreachable or returned an error: {e}")

