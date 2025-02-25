from abc import ABC, abstractmethod


class ILogWriter(ABC):
    """
    Abstract base class for log writers.

    This interface defines the contract for any log writer implementation,
    ensuring a consistent method for writing log data.
    """

    @abstractmethod
    def write_log(self, log: dict) -> None:
        """
        Writes the log data to the specified destination.

        Args:
            log (dict): The log data containing captured keystrokes and associated metadata.
        """
        pass
