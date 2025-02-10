from abc import ABC, abstractmethod


class KeyloggerInterface(ABC):
    """The KeyloggerInterface class is an abstract class that defines the interface for keylogger. It provides basic
    functionality and methods to implement by any keylogger mechanism.
    """

    @abstractmethod
    def start(self):
        """Keylogger starting."""
        pass

    @abstractmethod
    def stop(self):
        """Keylogger stopping."""
        pass

    @abstractmethod
    def get_log(self):
        """get the buffered log of the keystroke."""
        pass
