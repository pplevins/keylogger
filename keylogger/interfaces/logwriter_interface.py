from abc import ABC, abstractmethod


class LogWriterInterface(ABC):
    """The LogWriterInterface class is an abstract base class that the interface for the log writers. It provides basic
    functionality and methods to implement by any log writer mechanism.
    """

    @abstractmethod
    def write_log(self, log: str):
        """Writes the log data."""
        pass
