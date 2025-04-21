## Save and Clear DataBase Table at midnoght

print("J ========== START IMPORT 'save_clear_db.py'              ========== J")

import d_t_routs
import urequests
import machine
import time

import call_break

# Use RTC memory to store the last save day
rtc = machine.RTC()

## SAVE-CLEAR_url - used in 'def trigger_save_and_clear()',  row 48
# SAVE_CLEAR_url = "http://192.168.2.101/FMuBruwer/4-export-clear-script-fem1.php"
# SAVE_CLEAR_url = "http://192.168.2.101/FMuBruwer/4-export-clear-script-fem2.php"
# SAVE_CLEAR_url = "http://192.168.2.103/FMuBruwer/4-export-clear-script-fem2.php"
SAVE_CLEAR_url = "http://192.168.2.101/FMuBruwer/FMuBruwer-4.php"
# SAVE_CLEAR_url = "http://192.168.2.105/FMuBruwer/FMuBruwer-4.php"

# def get_last_save_day():
#    try:
#        return rtc.memory()[0]
#    except:
#        return 0  # Default to 0 if no memory is set

# def set_last_save_day(day):
##    rtc.memory(bytearray([day]))
#    print("NOT DOING IT HERE")


def is_near_midnight(time_str):
    # Extract hour, minute, second from the time string
    time_parts = time_str.split()
    if len(time_parts) != 2:
        return False
    time_only = time_parts[1]
    hour, minute, second = map(int, time_only.split(":"))

    SaveAndClear_hour = 23
    SaveAndClear_min = 59
    SaveAndClear_sec = 45
    Hrs_to_go = SaveAndClear_hour - hour
    Min_to_go = SaveAndClear_min - minute
    Sec_to_go = SaveAndClear_sec - second
    #    print(SaveAndClear_hour - hour)
    #    print("   ", Hrs_to_go, ":", Min_to_go, ":", Sec_to_go)
    print(
        f"│   Time to go - {Hrs_to_go:02d}:{Min_to_go:02d}:{Sec_to_go:02d}"
        + " " * (box_width - 24)
        + "│"
    )
    #    print(f"│ {hour:02d}:{minute:02d}:{second:02d}                    |")
    print("└" + "─" * box_width + "┘")

    # Check if time is between 23:59:45 and 00:00:14
    #    return (hour == 23 and minute == 12 and second >= 45) or \
    #           (hour == 0 and minute == 0 and second < 15)

    # Check if the time is between 11:45:45 and 11:45:59
    #    return (hour == 11 and minute == 45 and second >= 45)

    # Check if the time is between 23:59:45 and 23:59:59
    return hour == 23 and minute == 59 and second >= 45


def trigger_save_and_clear():
    #    print("scdb tsac @43 started - >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # Send request to your PHP script to save and clear the database
    #    url = "http://192.168.2.101/FMuBruwer/4-export-clear-script-fem1.php"
    #    url = "http://192.168.2.101/FMuBruwer/4-export-clear-script-fem2.php"

    try:
        #        response = urequests.get(url)
        response = urequests.get(SAVE_CLEAR_url)
        print("Save and clear triggered. Response:", response.text)
        print("=" * 80)

        response.close()
    except Exception as e:
        print("Error triggering save and clear:", str(e))


#    print("scdb tsac @55 ended - <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


def check_and_trigger_save():
    global text_1, box_width
    d_t_routs.get_now_time()  # This updates the global now_time variable
    time_str = d_t_routs.now_time

    #    print("Now at 'save_clear_db.py' 'def check_and_trigger_save()' - time_str is", time_str)

    # Print the boxed text
    text_1 = "Save and Clear database"
    box_width = len(text_1) + 2  # Adding 2 to account for box borders
    print("waiting ....", end="")
    time.sleep(0.02)  # Delay for a short moment (10 milliseconds)
    print("\r┌" + "─" * box_width + "┐")
    print("│ " + text_1 + " │")
    #    print("└" + "─" * box_width + "┘")
    #    call_break.c_break()
    # Extract the day from the date string
    current_day = int(time_str.split()[0].split("/")[2])
    # last_save_day = get_last_save_day()
    #    call_break.c_break()

    if is_near_midnight(time_str):  # and current_day != last_save_day:
        trigger_save_and_clear()
        # set_last_save_day(current_day)


# In your main loop, after sending data to db:
# send_data_to_db()
# check_and_trigger_save()

# check_and_trigger_save()


print("J ==========   END IMPORT 'save_clear_db.py'              ========== J")
