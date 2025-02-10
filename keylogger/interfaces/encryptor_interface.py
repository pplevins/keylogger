from abc import ABC, abstractmethod


class EncryptorInterface(ABC):
    """The EncryptorInterface class is an abstract base class
    that defines the interface for all Encryptor classes in use.
    It provides methods for encrypting and decrypting data for various types of encryption.
    """

    @abstractmethod
    def encrypt(self, data: str) -> str:
        """Encrypt data."""
        pass

    @abstractmethod
    def decrypt(self, data: str) -> str:
        """Decrypt data."""
        pass
