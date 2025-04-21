"""
Fermentation Chamber Temperature Controller - Main Program
Core temperature control and monitoring logic (refactored for clarity, PEP 8, and robustness).
"""

print("B ========== START IMPORT 'main_prog.py'                  ========== B")

import time
import machine
from machine import RTC

# Third-party imports (commented out if not used)
# import urequests
# import ujson

# Local imports
import display_drive
from wifi_connect import wifi_connect_time_sync, sync_time
import d_t_routs
from update_settings_from_server import update_settings_from_server
import settings
from te__relay_C_O_H__db__routs import get_tr_temps

# Configuration defaults
DEBUG_MODE = True
MAIN_LOOP_INTERVAL = 15  # seconds
DISPLAY_TOGGLE_INTERVAL_MS = 500  # milliseconds
WATCHDOG_BLIP_INTERVAL_MS = 1000  # milliseconds
SERVER_URL = "http://192.168.2.101/FMuBrewer/FMuBrewer-1.php"
LOCAL_SETTINGS_FILE = "fermenter_settings.ujson"

# Load configuration from config.json if available
try:
    import ujson

    with open("config.json") as f:
        config = ujson.load(f)
    DEBUG_MODE = config.get("DEBUG_MODE", DEBUG_MODE)
    MAIN_LOOP_INTERVAL = config.get("MAIN_LOOP_INTERVAL", MAIN_LOOP_INTERVAL)
    DISPLAY_TOGGLE_INTERVAL_MS = config.get(
        "DISPLAY_TOGGLE_INTERVAL_MS", DISPLAY_TOGGLE_INTERVAL_MS
    )
    WATCHDOG_BLIP_INTERVAL_MS = config.get(
        "WATCHDOG_BLIP_INTERVAL_MS", WATCHDOG_BLIP_INTERVAL_MS
    )
    SERVER_URL = config.get("SERVER_URL", SERVER_URL)
    LOCAL_SETTINGS_FILE = config.get("LOCAL_SETTINGS_FILE", LOCAL_SETTINGS_FILE)
    print("[INFO] Loaded configuration from config.json")
except Exception as exc:
    print(f"[WARNING] Could not load config.json: {exc}")
    # Continue with defaults

# RTC initialization
rtc = RTC()


def log(message: str, level: str = "INFO") -> None:
    """Simple logger for MicroPython environments."""
    print(f"[{level}] {message}")


class TemperatureController:
    """
    Controls the temperature regulation process, display feedback, and timing logic.
    """

    def __init__(self) -> None:
        self.loop = 0
        self.minute = 0
        self.hour = 0
        self.last_watchdog_reset = time.ticks_ms()
        self.last_display_toggle = time.ticks_ms()
        self.display_state = False
        self.series_loop = 1

    def watchdog_reset(self) -> None:
        """Reset the watchdog timer using display blip periodically."""
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_watchdog_reset) >= WATCHDOG_BLIP_INTERVAL_MS:
            display_drive.display_dp_blip()
            self.last_watchdog_reset = now

    def toggle_display(self) -> None:
        """Toggle display state for visual feedback periodically."""
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_display_toggle) >= DISPLAY_TOGGLE_INTERVAL_MS:
            self.display_state = not self.display_state
            if self.display_state:
                display_drive.display_dp_on()
            else:
                display_drive.display_dp_off()
            self.last_display_toggle = now

    def update_run_time(self) -> None:
        """Update and print run time information."""
        print("NOW AT main_prog.py ROW 88")
        d_t_routs.get_now_time()
        print("NOW AT main_prog.py ROW 90")
        if self.loop + self.minute + self.hour == 0:
            print("NOW AT main_prog.py ROW 92")
            d_t_routs.get_start_time()
            print("NOW AT main_prog.py ROW 94")
        self.loop += 1
        print("NOW AT main_prog.py ROW 96")
        get_tr_temps()
        print("NOW AT main_prog.py ROW 98")

        if self.loop == 4:
            self.loop = 0
            self.minute += 1
        if self.minute == 60:
            self.minute = 0
            self.hour += 1

        run_time_message = (
            f"Run Time: {self.hour} hrs, {self.minute} min, "
            f"{self.loop * MAIN_LOOP_INTERVAL} sec : "
            f"{d_t_routs.start_time} - {d_t_routs.now_time}"
        )
        log(run_time_message, level="INFO")
        print("╔" + "═" * (len(run_time_message) + 2) + "╗")
        print("║ " + run_time_message + " ║")
        print("╚" + "═" * (len(run_time_message) + 2) + "╝")

    def main_loop(self) -> None:
        """
        Main control loop: handles timing, measurement, display, and watchdog.
        """
        # Align to next MAIN_LOOP_INTERVAL
        current_time = rtc.datetime()
        current_seconds = current_time[5] * 60 + current_time[6]
        seconds_to_wait = (MAIN_LOOP_INTERVAL - 1) - (
            current_seconds % MAIN_LOOP_INTERVAL
        )
        if seconds_to_wait <= 0:
            seconds_to_wait += MAIN_LOOP_INTERVAL
        time.sleep(seconds_to_wait)
        print("NOW AT main_prog.py ROW 122")

        #        while True:
        #            try:
        #                current_time = rtc.datetime()
        #                current_seconds = current_time[5] * 60 + current_time[6]
        #
        #                # Run main tasks every MAIN_LOOP_INTERVAL seconds
        #                if current_seconds % MAIN_LOOP_INTERVAL == (MAIN_LOOP_INTERVAL - 1):
        #                    print("\n" * 4)
        #                    print("═" * 86)
        #                    d_t_routs.get_now_time()
        #                    message = f"Temperature and Status Measurement {self.series_loop} at: {d_t_routs.now_time}"
        #                    self.series_loop += 1
        #                    print("╔" + "═" * (len(message) + 2) + "╗")
        #                    print("║ " + message + " ║")
        #                    print("╚" + "═" * (len(message) + 2) + "╝")
        #                    self.update_run_time()
        #                    update_settings_from_server()
        #
        #                self.toggle_display()
        #                self.watchdog_reset()
        #                time.sleep_ms(10)  # Prevent excessive CPU usage
        #
        #            except Exception as exc:
        #                log(f"Error in main loop: {exc}", level="ERROR")
        #                traceback.print_exc()  # <-- Add this line
        #                self.watchdog_reset()
        #                time.sleep_ms(100)

        while True:
            #        try:
            current_time = rtc.datetime()
            current_seconds = current_time[5] * 60 + current_time[6]

            # Run main tasks every MAIN_LOOP_INTERVAL seconds
            if current_seconds % MAIN_LOOP_INTERVAL == (MAIN_LOOP_INTERVAL - 1):
                settings.load()  # <-- ADD THIS LINE
                print("\n" * 4)
                print("═" * 86)
                print("NOW AT main_prog.py ROW 162")
                d_t_routs.get_now_time()
                print("NOW AT main_prog.py ROW 164")
                message = f"Temperature and Status Measurement {self.series_loop} at: {d_t_routs.now_time}"
                self.series_loop += 1
                print("╔" + "═" * (len(message) + 2) + "╗")
                print("║ " + message + " ║")
                print("╚" + "═" * (len(message) + 2) + "╝")
                print("NOW AT main_prog.py ROW 170")
                self.update_run_time()
                print("NOW AT main_prog.py ROW 172")
                update_settings_from_server()
                print("NOW AT main_prog.py ROW 174")

            self.toggle_display()
            self.watchdog_reset()
            time.sleep_ms(10)  # Prevent excessive CPU usage

            #        except Exception as exc:
            #            log(f"Error in main loop: {exc}", level="ERROR")
            #            traceback.print_exc()  # <-- Add this line
            self.watchdog_reset()
            time.sleep_ms(100)


def main() -> None:
    """
    Entry point for the temperature controller. Initializes WiFi/time and starts the control loop.
    """
    log("Starting Temperature Controller...", level="INFO")
    wifi_ok = wifi_connect_time_sync()
    if not wifi_ok:
        log("WiFi/time sync failed. Retrying or entering safe mode...", level="WARNING")
        # Optionally retry or enter a safe state here
    controller = TemperatureController()
    try:
        controller.main_loop()
    except Exception as exc:
        log(f"Fatal error in main loop: {exc}", level="CRITICAL")
        # Optionally perform cleanup or safe shutdown here


if __name__ == "__main__":
    main()

print("B ==========   END IMPORT 'main_prog.py'                  ========== B")
