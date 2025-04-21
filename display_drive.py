"""
Display Driver for 7-Segment Display on ESP32
"""

print("C ========== START IMPORT 'display_drive.py'              ========== C")

from machine import Pin
import time

# Define GPIO pins for each segment and DP
segments = {
    "A": Pin(17, Pin.OUT),
    "B": Pin(18, Pin.OUT),
    "C": Pin(19, Pin.OUT),
    "D": Pin(21, Pin.OUT),
    "E": Pin(22, Pin.OUT),
    "F": Pin(23, Pin.OUT),
    "G": Pin(25, Pin.OUT),
    "DP": Pin(26, Pin.OUT),
}

# Segment states for each character (update as needed)
characters = {
    "H": {"A": 1, "B": 0, "C": 0, "D": 1, "E": 0, "F": 0, "G": 0, "DP": 1},
    "C": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 1, "F": 1, "G": 1, "DP": 1},
    "O": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 1, "DP": 1},
    "h": {"A": 1, "B": 0, "C": 0, "D": 1, "E": 1, "F": 0, "G": 0, "DP": 1},
    "c": {"A": 0, "B": 0, "C": 1, "D": 1, "E": 1, "F": 1, "G": 0, "DP": 1},
    "x": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1, "DP": 1},
}


def display_char(char):
    """
    Display a single character on the 7-segment display.

    Args:
        char (str): Character to display. Must be a key in characters.
    Raises:
        ValueError: If the character is not supported.
    """
    if char not in characters:
        raise ValueError(f"Unsupported character: {char}")
    for segment, state in characters[char].items():
        segments[segment].value(state)


def display_dp_on():
    """Turn the decimal point (DP) segment ON."""
    segments["DP"].value(0)


def display_dp_off():
    """Turn the decimal point (DP) segment OFF."""
    segments["DP"].value(1)


def display_dp_blip(duration_ms=150):
    """
    Blink the decimal point (DP) segment briefly for visual feedback.

    Args:
        duration_ms (int): Duration in milliseconds to keep DP on.
    """
    display_dp_on()
    time.sleep_ms(duration_ms)
    display_dp_off()


def flash_dp_forever():
    """Continuously flash the decimal point segment (for test/demo)."""
    while True:
        display_dp_on()
        time.sleep(1)
        display_dp_off()
        time.sleep(1)


if __name__ == "__main__":
    # Example test/demo usage
    display_char("H")
    flash_dp_forever()

print("C ==========   END IMPORT 'display_drive.py'              ========== C")
