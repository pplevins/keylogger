import os
from datetime import datetime

from keylogger.interfaces import LogWriterInterface


class FileLogWriter(LogWriterInterface):
    """Writes logs to a txt file."""

    def __init__(self, file_name='logfile'):
        self.file_path = f'logs/{file_name}.txt'
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Checks if the file exists, and creates it if not."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(f"--- Log File Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

    def write_log(self, log):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}]\n")
            for key, text in log.items():
                file.write(f"on {key} window: " + text + "\n")
