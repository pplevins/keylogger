from keylogger.interfaces import EncryptorInterface


class XorEncryption(EncryptorInterface):
    """
    Implements simple XOR encryption.

    This encryption method applies XOR between each character of the input
    string and the corresponding character in the key (cycled if necessary).
    """

    def __init__(self, key: str = "my_secret_key"):
        """
        Initializes the XOR encryptor with a given key.

        Args:
            key (str): The encryption key. Must be a non-empty string.

        Raises:
            ValueError: If the key is empty.
        """
        if not key:
            raise ValueError("Encryption key must not be empty.")
        self.key = key

    def encrypt(self, data: str) -> str:
        """
        Encrypts the given string using XOR.

        Args:
            data (str): The plaintext string to encrypt.

        Returns:
            str: The encrypted data represented as integers in a string.

        Note:
            XOR is reversible, meaning the same method can be used for decryption (not in our case).
        """
        return "-".join(str(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data))

    def decrypt(self, data: str) -> str:
        """
        Decrypts the given string using XOR.

        Args:
            data (str): The encrypted data represented as integers in a string.

        Returns:
            str: The decrypted plaintext.
        Note:
            Since XOR is symmetrical, the same function is used for both encryption and decryption (not in our case).
        """
        return "".join(chr(int(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data.split("-")))

    def _recursive_encrypt_dict(self, enc_func, logs_dict: dict, encrypted_dict: dict) -> None:
        """
        Recursively encrypts a nested dictionary.

        Args:
            enc_func (Callable[[str], str]): The encryption function.
            logs_dict (dict): The dictionary containing data to encrypt.
            encrypted_dict (dict): The output dictionary where encrypted data is stored.

        Note:
            This function is used internally to support dictionary encryption.
        """
        for key, value in logs_dict.items():
            enc_key = enc_func(key)  # Encrypt the key

            if isinstance(value, dict):
                encrypted_dict[enc_key] = {}
                self._recursive_encrypt_dict(enc_func, value, encrypted_dict[enc_key])
            else:
                encrypted_dict[enc_key] = enc_func(value)

    def get_encrypted_dict(self, enc_func, logs_dict: dict) -> dict:
        """
        Encrypts all keys and values of a dictionary using the given encryption function.

        Args:
            enc_func (Callable[[str], str]): The encryption function to use.
            logs_dict (dict): The dictionary containing data to encrypt.

        Returns:
            dict: A new dictionary with all keys and values encrypted.
        """
        encrypted_dict = {}
        self._recursive_encrypt_dict(enc_func, logs_dict, encrypted_dict)
        return encrypted_dict
