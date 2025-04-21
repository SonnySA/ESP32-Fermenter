print("F ========== START IMPORT 'import d_t_routs.py'           ========== F")

# this is 'd_t_routs.py'
# date and time routines

import machine
import time

# Initialize the RTC
rtc = machine.RTC()


# ================================================================================
# Function to set RTC with specific date and time
def pre_set_rtc_datetime() -> None:
    """
    Set the RTC to a predefined date and time for testing/demo purposes.
    Calls set_rtc_datetime with hardcoded values and prints the result.
    """
    new_year = 2023
    new_month = 5
    new_day = 27
    new_hour = 14
    new_minute = 29
    new_second = 59
    set_rtc_datetime(new_year, new_month, new_day, new_hour, new_minute, new_second)
    print_rtc_datetime()


# ================================================================================
def set_rtc_datetime(
    year: int, month: int, day: int, hour: int, minute: int, second: int
) -> None:
    """
    Set the RTC date and time to the specified values.
    Args:
        year (int): Year value
        month (int): Month value
        day (int): Day value
        hour (int): Hour value
        minute (int): Minute value
        second (int): Second value
    """
    rtc.datetime((year, month, day, 0, hour, minute, second, 0))


# ================================================================================
def print_rtc_datetime() -> None:
    """
    Print the current RTC date and time in a human-readable format.
    Includes weekday and month names.
    """
    rtc_datetime = rtc.datetime()
    year = rtc_datetime[0]
    month = rtc_datetime[1]
    day = rtc_datetime[2]
    weekday = rtc_datetime[3]
    hour = rtc_datetime[4]
    minute = rtc_datetime[5]
    second = rtc_datetime[6]

    def weekday_name(day: int) -> str:
        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        return weekdays[day]

    def month_name(month: int) -> str:
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        return months[month - 1]

    print("--------------------------------------------------")
    print(
        f"Current RTC status: {weekday_name(weekday)} {month_name(month)} {day}, {year}  {hour:02}:{minute:02}:{second:02}"
    )
    print("--------------------------------------------------\n")


# ================================================================================
start_time = None


def get_start_time() -> str:
    """
    Get the current RTC date and time as a formatted string (start time).
    Assigns the result to the global variable start_time and also returns it.
    Returns:
        str: Formatted date and time string 'YYYY/MM/DD HH:MM:SS'.
    """
    global start_time
    rtc = machine.RTC()
    time_start = rtc.datetime()
    start_time = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        time_start[0],
        time_start[1],
        time_start[2],
        time_start[4],
        time_start[5],
        time_start[6],
    )
    return start_time


# ================================================================================
now_time = None


def get_now_time() -> str:
    """
    Get the current RTC date and time as a formatted string (now time).
    Assigns the result to the global variable now_time and also returns it.
    Returns:
        str: Formatted date and time string 'YYYY/MM/DD HH:MM:SS'.
    """
    global now_time
    rtc = machine.RTC()
    time_now = rtc.datetime()
    now_time = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        time_now[0], time_now[1], time_now[2], time_now[4], time_now[5], time_now[6]
    )
    return now_time
    # ================================================================================


# pre_set_rtc_datetime()
##set_rtc_datetime(year, month, day, hour, minute, second)
# print_rtc_datetime()
# get_start_time()
# get_now_time()
# print(now_time)
# print("====== 'dt_routs.py' loaded ======")
# print()
# print()

print("F ==========   END IMPORT 'import d_t_routs.py'           ========== F")
