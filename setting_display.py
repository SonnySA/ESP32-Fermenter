"""
setting_display.py
Module for displaying wort setpoint and related temperatures.
"""

from display import wait, box_sep, box_bottom


def display_wort_setting(wort_set, wort_temp, chamber_temp):
    """Display a boxed summary of wort setpoint and current temps."""
    text = f"Wort Temp Setting: {wort_set:.3f}, Wort Temp: {wort_temp:.3f}, Chamber Temp: {chamber_temp:.3f}"
    box_width = len(text) + 2  # margins
    wait()
    box_sep(box_width)
    print(f"│ {text} │")
    box_bottom(box_width)
