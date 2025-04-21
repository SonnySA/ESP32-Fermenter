"""
Fermentation Chamber Temperature Controller - Main Program
This is the entry point for the ESP32-based temperature control system.
"""

print("A ========== START IMPORT 'main.py'                       ========== A")

"""
Fermentation Chamber Temperature Controller - Main Program
Entry point for the ESP32-based temperature control system.
"""

import time
import machine
import gc
from machine import Pin
import main_prog
import display_drive
import wifi_connect
import settings

# Configuration
DEBUG_MODE = True
INITIALIZATION_DELAY_MS = 200
WATCHDOG_BLIP_DELAY_MS = 200  # Delay between watchdog resets


def watchdog_reset(display):
    """Reset the watchdog timer using display blip."""
    try:
        if display:
            display.display_dp_blip()
            time.sleep_ms(WATCHDOG_BLIP_DELAY_MS)
    except Exception as exc:
        print(f"Watchdog reset error: {exc}")


def init_display():
    """Initialize and test the display."""
    try:
        display_drive.display_dp_on()
        time.sleep_ms(INITIALIZATION_DELAY_MS)
        display_drive.display_dp_off()
        return display_drive
    except Exception as exc:
        print(f"Display initialization error: {exc}")
        return None


def init_wifi(display):
    """Initialize WiFi connection."""
    try:
        watchdog_reset(display)
        return wifi_connect
    except Exception as exc:
        print(f"WiFi initialization error: {exc}")
        return None


def init_system():
    """Initialize all system components."""
    # Initialize display first for visual feedback and watchdog
    display = init_display()
    if not display:
        print("Warning: Display initialization failed")

    # Initialize WiFi with watchdog reset
    wifi = init_wifi(display)
    if not wifi:
        print("Warning: WiFi initialization failed")

    # Run garbage collection
    gc.collect()

    return display, wifi


def main():
    """Main program entry point"""
    print("Starting Fermentation Chamber Controller...")

    # Initialize system components
    display, wifi = init_system()

    # Reset watchdog before starting main program
    watchdog_reset(display)

    if DEBUG_MODE:
        print("System initialization complete")
        print(f"Free memory: {gc.mem_free()} bytes")

    # Reset watchdog after successful initialization
    watchdog_reset(display)

    # Call the main function from main_prog
    main_prog.main()  # This line remains unchanged


if __name__ == "__main__":
    main()

print("A ========== START IMPORT 'main.py'                       ========== A")
