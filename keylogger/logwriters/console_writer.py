from datetime import datetime

from keylogger.interfaces import LogWriterInterface


class ConsoleLogWriter(LogWriterInterface):
    """Writes logs to the console."""

    def write_log(self, log):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Keystrokes: {log}")
