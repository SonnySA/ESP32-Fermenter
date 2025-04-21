"""
mode_display.py
Module for mapping control modes to 7-segment display characters.
"""

from display_drive import display_char

# Mapping of mode numbers to display characters
_mode_map = {
    0: "O",  # IDLE
    1: "C",  # COOLING
    2: "c",  # COOL_REST
    3: "H",  # HEATING
    4: "h",  # HEAT_REST
}


def display_mode_char(mode_number):
    """
    Display the given mode on the 7-segment display.
    Falls back to an error print if unsupported.
    """
    char = _mode_map.get(mode_number)
    if char is not None:
        display_char(char)
    else:
        print(f"Invalid mode for display: {mode_number}")
