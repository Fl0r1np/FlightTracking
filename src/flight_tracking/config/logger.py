import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from flight_tracking.config.settings import Config

# Settings
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Custom TimedRotatingFileHandler
# - Rotates at midnight every day
# - backupCount=7 keeps the last 7 days of logs and automatically deletes older ones
file_handler = TimedRotatingFileHandler(
    filename = LOG_FILE,
    when = "midnight",
    interval = 1,
    backupCount = 7,
    encoding = "utf-8"
)
file_handler.suffix = "%Y-%m-%d"

# StreamHandler for stdout
stream_handler = logging.StreamHandler(sys.stdout)

# Basic Configuration
logging.basicConfig(
    level = Config.LOGGING_LEVEL,
    format = "%(asctime)s | %(levelname)s | %(module)s | %(message)s",
    handlers = [
        file_handler,
        stream_handler
    ]
)

# Export a logger instance to be imported by other modules
logger = logging.getLogger(__name__)