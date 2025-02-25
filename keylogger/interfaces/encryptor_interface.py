from abc import ABC, abstractmethod


class IEncryptor(ABC):
    """
    Abstract base class for encryption implementations.

    This interface defines the contract for encryption and decryption operations
    that all encryptor classes must follow.
    """

    @abstractmethod
    def encrypt(self, data: str) -> str:
        """
        Encrypts the given data.

        Args:
            data (str): The plaintext string to be encrypted.

        Returns:
            str: The encrypted representation of the input data.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass

    @abstractmethod
    def decrypt(self, data: str) -> str:
        """
        Decrypts the given data.

        Args:
            data (str): The encrypted string to be decrypted.

        Returns:
            str: The decrypted plaintext.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass
