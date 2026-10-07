import os
from datetime import datetime, timezone
import logging
import json
from flight_tracking.config.settings import Config

logger = logging.getLogger(__name__)


class Storage:

    def __init__(self):
        self.storage_location = Config.RAW_DATA_DIR


    def save_raw_data(self, raw_json: dict):
        """
        Save the raw json data to the storage
        :param raw_json: The raw json data represented as a dictionary
        :return: Nothing
        """

        logger.info(f"Starting to save the raw json data to {self.storage_location}.")

        # Build the file path
        current_datetime = datetime.now(timezone.utc)
        year = current_datetime.strftime('%Y')
        month = current_datetime.strftime('%m')
        day = current_datetime.strftime('%d')
        time_str = current_datetime.strftime('%H%M%S')
        file_path = os.path.join(
            self.storage_location,
            f"year={year}",
            f"month={month}",
            f"day={day}",
            f"flight_states_{time_str}.json"
        )

        # Create the directory safely
        directory_path = os.path.dirname(file_path)
        os.makedirs(directory_path, exist_ok=True)

        # Save the file to disk
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(raw_json, file, indent=4)  # indent=4 => human-readable

        logger.info(f"Successfully saved the raw json data to {file_path}.")

storage = Storage()