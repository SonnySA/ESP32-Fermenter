"""
sensor_display.py
Module to print sensor temperature tables.
"""

from display import wait, box_sep, box_bottom


def display_sensor_table(temps, avg_temps, sensor_labels):
    """Prints a boxed table of current and average temps for given sensors.
    sensor_labels: list of (label, rom_str) tuples."""
    # Define table width based on header
    header = "Sensor      | Current Temp | Average Temp"
    # Total width = header length + 2 spaces margin (one on each side)
    width = len(header) + 2

    wait()
    box_sep(width)
    print(f"│ {header} │")
    print(f"│ {'─'*len(header)} │")

    for label, rom in sensor_labels:
        if rom in temps:
            current = temps[rom]
            avg = avg_temps.get(rom, current)
            print(f"│ {label:<12}| {current:>12.3f} | {avg:>12.3f} │")

    box_bottom(width)
