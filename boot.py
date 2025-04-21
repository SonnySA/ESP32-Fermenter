# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)

print("========== START OF BOOT   ===========")

import os, machine

# os.dupterm(None, 1) # disable REPL on UART(0)
import gc
import utime
import webrepl
from machine import RTC

# Configuration
WEBREPL_ENABLED = True  # Set to False to disable WebREPL
DEBUG_MODE = True  # Set to False for production


def init_rtc():
    """Initialize and return the RTC with current time"""
    start_time = utime.ticks_us()  # Start timing

    try:
        rtc = RTC()
        rtc_datetime = rtc.datetime()
        if DEBUG_MODE:
            print("--------------------------------------")
            print(
                "RTC Date and Time:",
                "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                    rtc_datetime[0],
                    rtc_datetime[1],
                    rtc_datetime[2],
                    rtc_datetime[4],
                    rtc_datetime[5],
                    rtc_datetime[6],
                ),
            )
            print("--------------------------------------")
            # Calculate and print timing
            end_time = utime.ticks_us()
            duration = utime.ticks_diff(end_time, start_time)
            print(f"RTC initialization took {duration} microseconds")
        return rtc
    except Exception as e:
        end_time = utime.ticks_us()
        duration = utime.ticks_diff(end_time, start_time)
        print(f"Error initializing RTC: {e}")
        print(f"Error handling took {duration} microseconds")
        return None


def init_webrepl():
    """Initialize WebREPL if enabled"""
    if WEBREPL_ENABLED:
        start_time = utime.ticks_us()  # Start timing
        try:
            webrepl.start()
            if DEBUG_MODE:
                print("WebREPL started successfully")
                # Calculate and print timing
                end_time = utime.ticks_us()
                duration = utime.ticks_diff(end_time, start_time)
                print(f"WebREPL initialization took {duration} microseconds")
        except Exception as e:
            end_time = utime.ticks_us()
            duration = utime.ticks_diff(end_time, start_time)
            print(f"Error starting WebREPL: {e}")
            print(f"Error handling took {duration} microseconds")


def main():
    """Main boot sequence"""
    # Disable debug output if not in debug mode
    if not DEBUG_MODE:
        import esp

        esp.osdebug(None)

    # Initialize components
    rtc = init_rtc()
    init_webrepl()

    # Run garbage collection
    gc.collect()

    if DEBUG_MODE:
        print(f"Free memory: {gc.mem_free()} bytes")
        print("==========   END OF BOOT   ===========")
        print()


if __name__ == "__main__":
    main()
