import json
import os

from keylogger.interfaces import LogWriterInterface


class JsonLogWriter(LogWriterInterface):
    """
    Writes logs to a json file in a structured format.

    This class appends new log entries with timestamps and organizes them per application in the json format.
    """

    def __init__(self, file_name='logfile'):
        """Initializes the log writer and ensures the log file exists."""
        self.file_path = f'logs/{file_name}.json'
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the log file exists, creating it if necessary."""

        # Make sure the directory 'logs' exists, else creating it.
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump({}, file)

    def write_log(self, log: dict) -> None:
        """
        Writes the log data to the file in a structured format.

        Args:
            log (dict): A dictionary containing captured keystrokes organized by application and timestamps.
        """
        if not log:
            return  # No log to write

        # Loading the json file into a dictionary.
        with open(self.file_path, "r", encoding="utf-8") as file:
            logs = json.load(file)
        logs.update(log)  # Merging the two dictionaries into one.

        # Updating the json file with the new data.
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=4, ensure_ascii=False)
