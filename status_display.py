"""
status_display.py
Module for printing phase and environment temperature boxes.
"""

from display import wait, box_sep, box_bottom


def display_phase(text):
    """Print a single-line boxed status phase."""
    box_width = len(text) + 2
    wait()
    box_sep(box_width)
    print(f"│ {text} │")
    box_bottom(box_width)


def display_env_and_limits(wort_temp, chamber_temp, outside_temp, params):
    """Print a boxed two-line display: current temps and parameter limits."""
    header = f"Temperatures - Wort: {wort_temp:.2f}, Chamber: {chamber_temp:.2f}, Outside: {outside_temp:.2f}"
    limits = (
        f"Temperature Limits - CON: {params['cool_on']:.3f}, COF: {params['cool_off']:.3f}, "
        f"HON: {params['heat_on']:.3f}, HOF: {params['heat_off']:.3f}"
    )
    lines = [header, limits]
    maxw = max(len(l) for l in lines)
    box_width = maxw + 2

    wait()
    box_sep(box_width)
    for l in lines:
        print(f"│ {l:<{maxw}} │")
    box_bottom(box_width)
