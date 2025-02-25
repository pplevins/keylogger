from abc import ABC, abstractmethod


# TODO: change name conventions in all interfaces to Java convention (IEncryptor, IWriter, etc.)
class KeyloggerInterface(ABC):
    """
    Abstract base class for a keylogger.

    This interface defines the basic methods required for a keylogger implementation,
    ensuring that any concrete class will provide necessary functionality.
    """

    @abstractmethod
    def start(self) -> None:
        """
        Starts the keylogger.

        This method should initialize the keylogging mechanism and begin capturing keystrokes.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stops the keylogger.

        This method should terminate the keylogging process and ensure proper cleanup.
        """
        pass

    @abstractmethod
    def get_log(self) -> dict:
        """
        Retrieves the buffered log of recorded keystrokes.

        Returns:
            dict: A dictionary representation of all logged keystrokes ,formatted in a dictionary.
        """
        pass
