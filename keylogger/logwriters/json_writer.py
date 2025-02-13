import json
import os
from datetime import datetime

from keylogger.interfaces import LogWriterInterface


class JsonLogWriter(LogWriterInterface):
    """Writes logs to a json file."""

    def __init__(self, file_name='logfile'):
        self.file_path = f'logs/{file_name}.json'
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Checks if the file exists, and creates it if not."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump({}, file)

    def write_log(self, log):
        with open(self.file_path, "r", encoding="utf-8")as file:
            logs = json.load(file)
        logs.update(log)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=4, ensure_ascii=False)