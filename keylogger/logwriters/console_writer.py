from keylogger.interfaces import LogWriterInterface


class ConsoleLogWriter(LogWriterInterface):
    """
    Writes logs to the console in a human-readable format.

    This class takes log data with timestamps, formats it and prints it in a readable form.
    """

    def write_log(self, log: dict) -> None:
        """
        Writes the log data to the console in a structured format.

        Args:
            log (dict): The dictionary containing captured keystrokes and associated metadata.
        """
        if not log:
            print("No new logs to display.")
            return

        for timestamp, logs in log.items():
            print("\n" + "=" * 50)
            print(timestamp)
            print("=" * 50)

            for window, keystrokes in logs.items():
                print(f"\n[Application: {window}]")
                print(f"Keystrokes: {keystrokes}")

        print("=" * 50 + "\n")
