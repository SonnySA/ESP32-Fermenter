"""
display.py
Module for printing formatted boxes and waiting prompts.
"""

import time


def wait():
    """Prints 'waiting ....' with a short delay before display updates."""
    print("waiting ....", end="")
    time.sleep(0.02)


def box_top(text):
    """Print a top box line around the provided text."""
    print(f"\r┌ {text} ┐")


def box_sep(width):
    """Print a separator box line of the given width (number of dashes)."""
    print(f"\r┌{'─' * width}┐")


def box_bottom(width):
    """Print a bottom box line of the given width (number of dashes)."""
    print(f"└{'─' * width}┘")
