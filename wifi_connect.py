"""
WiFi Connection and Time Synchronization Module for ESP32

Handles WiFi initialization, connection, scanning, and NTP time sync.
"""

print("D ========== START IMPORT 'wifi_connect.py'               ========== D")

import time
import machine
import network
import ntptime
from debug_config import debug_1_print
import display_drive

# Constants
SA_TZ_OFFSET = 2 * 3600  # South Africa timezone offset (seconds)
WIFI_NETWORKS = [
    ("UPSTAIRS#2", "0118276422"),
    ("UPSTAIRS", "0118272328"),
    #    ("Zyxel_A151", "0118272328"),
    ("Home_Network", "0118276422"),
]


def _display_rtc_datetime():
    """Display and print the current RTC date and time."""
    rtc = machine.RTC()
    rtc_datetime = rtc.datetime()
    print(" " + "_" * 40)
    print(
        "│ RTC Date and Time: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} │".format(
            rtc_datetime[0],
            rtc_datetime[1],
            rtc_datetime[2],
            rtc_datetime[4],
            rtc_datetime[5],
            rtc_datetime[6],
        )
    )
    print(" " + "¯" * 40)


def _display_feedback():
    """Provide brief feedback via the display's decimal point."""
    display_drive.display_dp_on()
    time.sleep_ms(100)
    display_drive.display_dp_off()


def init_wlan():
    """
    Initialize and activate the WLAN interface.

    Returns:
        WLAN interface object if successful, else None.
    """
    debug_1_print("=== init_wlan() start ===")
    print("Initializing WLAN interface")
    _display_feedback()
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        print("WLAN interface initialized and activated")
        return wlan
    except (OSError, Exception) as exc:
        print(f"Error initializing WLAN: {exc}")
        return None


def scan_networks(wlan):
    """
    Scan for available WiFi networks and print results.

    Args:
        wlan: Initialized WLAN interface.
    Returns:
        List of scan results (each is a tuple with SSID, etc.), or empty list on error.
    """
    debug_1_print("=== scan_networks() start ===")
    print("Scanning for WiFi networks...")
    _display_feedback()
    try:
        scan_result = wlan.scan()
        if scan_result:
            print("Available Networks:")
            print(f"{'SSID':<30} Signal Strength (dBm)")
            print("-" * 50)
            for net in scan_result:
                ssid = (
                    net[0].decode("utf-8") if isinstance(net[0], bytes) else str(net[0])
                )
                rssi = str(net[3])
                print(f"{ssid:<30} {rssi}")
        else:
            print("No networks found.")
        return scan_result
    except (OSError, Exception) as exc:
        print(f"Error during network scan: {exc}")
        return []


def connect_to_best_wifi(wlan, networks=WIFI_NETWORKS, timeout=10):
    """
    Attempt to connect to the best available WiFi network from the known list.

    Args:
        wlan: Initialized WLAN interface.
        networks: List of (SSID, password) tuples.
        timeout: Timeout in seconds for each connection attempt.
    Returns:
        True if connection is successful, False otherwise.
    """
    debug_1_print("=== connect_to_best_wifi() start ===")
    available = scan_networks(wlan)
    available_ssids = [
        net[0].decode("utf-8") if isinstance(net[0], bytes) else str(net[0])
        for net in available
    ]
    for ssid, password in networks:
        if ssid in available_ssids:
            print(f"Attempting to connect to SSID: {ssid}")
            wlan.connect(ssid, password)
            for _ in range(timeout * 10):
                if wlan.isconnected():
                    print(f"Connected to {ssid}")
                    print(f"Network config: {wlan.ifconfig()}")
                    _display_feedback()
                    return True
                time.sleep(0.1)
            print(f"Failed to connect to {ssid}")
    print("Could not connect to any known WiFi network.")
    return False


def get_current_ssid(wlan):
    """
    Retrieve the SSID of the currently connected WiFi network.

    Args:
        wlan: Initialized WLAN interface.
    Returns:
        SSID (str) if connected, None otherwise.
    """
    if wlan.isconnected():
        try:
            return wlan.config("essid")
        except Exception as exc:
            print(f"Error retrieving SSID: {exc}")
            return None
    return None


def sync_time(max_retries=3, delay=2):
    """
    Synchronize the system time with an NTP server and update the RTC.

    Returns:
        True if time synchronization is successful, False otherwise.
    """
    debug_1_print("=== sync_time() start ===")
    for attempt in range(max_retries):
        try:
            ntptime.host = "pool.ntp.org"
            ntptime.settime()
            tm = time.localtime(time.time() + SA_TZ_OFFSET)
            machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
            print("Time synchronized successfully.")
            _display_rtc_datetime()
            return True
        except (OSError, Exception) as exc:
            print(f"NTP time sync failed (attempt {attempt+1}/{max_retries}): {exc}")
            time.sleep(delay)
    return False


def format_time(dt):
    """
    Format a datetime tuple from the RTC into a human-readable string.

    Args:
        dt (tuple): RTC datetime tuple (year, month, day, weekday, hour, minute, second, subsecond)
    Returns:
        str: Formatted date and time string (YYYY-MM-DD HH:MM:SS)
    """
    try:
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            dt[0], dt[1], dt[2], dt[4], dt[5], dt[6]
        )
    except Exception as exc:
        print(f"Error formatting time: {exc}")
        return "Invalid time"


def wifi_connect_time_sync():
    """
    Attempt to connect to the best available WiFi network and synchronize time.
    Provides user feedback via display and console. Continues regardless of success.
    """
    wlan = init_wlan()
    if wlan is None:
        print("WLAN initialization failed.")
        return False
    if not connect_to_best_wifi(wlan):
        print("WiFi connection failed.")
        return False
    print("WiFi connected. Waiting for network to settle before NTP sync...")
    time.sleep(2)  # Delay to allow network stack to settle
    if not sync_time():
        print("Time synchronization failed.")
        return False
    print("WiFi connected and time synchronized.")
    return True


def _display_feedback() -> None:
    """Blink the display decimal point for visual feedback."""
    display_drive.display_dp_on()
    time.sleep_ms(100)
    display_drive.display_dp_off()

    # -----------------------------------------------------------

    print("Could not connect to any WiFi network")
    debug_1_print(
        "=== 'WiFi_Connect.py - connect_to_best_wifi()' rout end   === " + "<" * 40
    )
    print("End of WiFi connection process")
    return False


# -----------------------------------------------------------
def get_current_ssid() -> str | None:
    """
    Retrieve the SSID of the currently connected WiFi network.
    Returns:
        SSID (str) if connected, None otherwise.
    """
    debug_1_print(
        "=== 'WiFi_Connect.py - get_current_ssid()' rout start === " + ">" * 40
    )
    _display_feedback()
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        return wlan.config("essid")
    return None
    # debug_1_print intentionally omitted after return for clarity


# -----------------------------------------------------------
# Get & update SA time
def sync_time() -> bool:
    """
    Synchronize the system time with an NTP server and update the RTC.
    Returns:
        True if time synchronization is successful, False otherwise.
    """
    debug_1_print("=== 'WiFi_Connect.py - sync_time()' rout start === " + ">" * 40)
    _display_feedback()
    print("sync_time() start")
    try:
        ntptime.settime()  # Set system time from NTP
        utc_time = time.localtime(time.time() + SA_TZ_OFFSET)
        rtc = machine.RTC()  # Instantiate RTC before use
        # Update the RTC with the adjusted local time
        rtc.datetime(
            (
                utc_time[0],
                utc_time[1],
                utc_time[2],
                utc_time[6] + 1,
                utc_time[3],
                utc_time[4],
                utc_time[5],
                0,
            )
        )
        print(" " + "_" * 57)
        print(f"│ Time synchronized. Current SA time: {format_time(rtc.datetime())} │")
        print(" " + "¯" * 57)
        return True
    except Exception as e:
        print(f"Time sync failed: {e}")
        return False
    debug_1_print("=== 'WiFi_Connect.py - sunc_time()' rout end   === " + "<" * 40)


# -----------------------------------------------------------
def format_time(dt: tuple) -> str:
    """
    Format a datetime tuple from the RTC into a human-readable string.
    Args:
        dt (tuple): RTC datetime tuple (year, month, day, weekday, hour, minute, second, subsecond)
    Returns:
        str: Formatted date and time string (YYYY-MM-DD HH:MM:SS)
    """
    # debug_1_print intentionally omitted for brevity
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        dt[0], dt[1], dt[2], dt[4], dt[5], dt[6]
    )


# -----------------------------------------------------------
# def wifi_conn_time_sync():
#    while True:
#        if connect_to_best_wifi():
#            if sync_time():
#                print("Time sync successful")
#            else:
#                print("Time sync failed, but continuing...")
#        else:
#            print("WiFi connection failed, but continuing...")

# -----------------------------------------------------------

# ========================================================================

debug_1_print("=== 'WiFi_Connect.py' import end   === " + "<" * 40)
# (Removed global print and sleep for clean startup)

import settings

if __name__ == "__main__":
    print("Starting WiFi connection and time sync demo...")
    success = wifi_connect_time_sync()
    if success:
        wlan = network.WLAN(network.STA_IF)
        print(f"Connected to WiFi network: {get_current_ssid(wlan)}")
    else:
        print("WiFi connection and/or time synchronization failed.")
    # Visual feedback (blink display)
    display_drive.display_dp_on()
    time.sleep_ms(100)
    display_drive.display_dp_off()

print("D ==========   END IMPORT 'wifi_connect.py'               ========== D")
