# update_settings_from_server() 240805 17:45
print("G ========== START IMPORT 'update_settings_from_server.py'========== G")

import call_break

import urequests
import ujson
import utime
import sys
import time

# call_break.c_break()
# Define the path and URL
import settings

# LOCAL_SETTINGS_FILE is now managed by settings.py
LOCAL_SETTINGS_FILE = "fermenter_settings.ujson"
# print("u_s_f_s @ 15")

""" List of available servers which may be used """
# SERVER_URL = "http://192.168.2.40/esp_control_try4/get_fermenter_settings_wp.php"
# SERVER_URL = "http://192.168.2.40/FMuBruwer/get_fermenter_settings_wp.php"
# SERVER_URL = "http://192.168.2.101/FMuBruwer/1-get_fermenter_settings_wp.php"
# SERVER_URL = "http://192.168.2.105/FMuBruwer/1-get_fermenter_settings_wp.php"
SERVER_URL = "http://192.168.2.101/FMuBruwer/FMuBruwer-1.php"
# SERVER_URL = "http://192.168.2.105/FMuBruwer/FMuBruwer-1.php"

# print("usfs @ 21")
# call_break.c_break()
# Initialize global settings
COLD_SETTINGS = {}
WARM_SETTINGS = {}
OTHER_SETTINGS = {}
######################################################################################
global usfs_loop
usfs_loop = -8


# Define a function to print a string inside a box
def print_in_box(text):
    # print("usfs 27")
    # Ensure that the input is always treated as a string
    if not isinstance(text, str):
        text = str(text)

    lines = text.split("\n")

    # Calculate the length of the longest line
    max_length = max(len(line) for line in lines)

    print("waiting", end="")
    time.sleep(0.02)  # Delay for a short moment (10 milliseconds)
    # Print the top border with angle corners
    print("\r┌" + "─" * (max_length + 2) + "┐")
    #    print("┌" + "─" * (max_length + 2) + "┐")
    # Print each line inside the box
    for line in lines:
        formatted_line = "│ " + line + " " * (max_length - len(line)) + " │"
        print(formatted_line)

    # Print the bottom border with angle corners
    print("└" + "─" * (max_length + 2) + "┘")
    print("═" * 86)


######################################################################################
# ===============================================================================#
def update_settings_from_server():

    global usfs_loop

    #    print("usfs_loop is", usfs_loop, end=" : ")
    #    usfs_loop = usfs_loop + 1
    #    print("u_s_f_s.u_s_f_s @ 61")
    try:
        # Load the current local settings and get the last modified time
        local_settings = settings.all()

        local_last_modified = local_settings.get("last_modified", 0)
        #        print("local_last_modfied is :", local_last_modified)

        # Convert timestamp to tuple (# 946684800 is seconds from 1970 to 2000)
        #  7200 is seconds from GMT to SA time - +2 hrs.
        #  MicroPython's utime.localtime() expects the timestamp to be in
        #   seconds since January 1, 2000, not since 1970 (Unix epoch).
        time_tuple = utime.localtime(local_last_modified - 946684800 + 7200)

        # Format the date string
        local_last_modified_date = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
            time_tuple[0],  # Year
            time_tuple[1],  # Month
            time_tuple[2],  # Day
            time_tuple[3],  # Hour
            time_tuple[4],  # Minute
            time_tuple[5],  # Second
        )

        # Fetch settings from server
        response = urequests.get(SERVER_URL, timeout=10)
        server_data = response.json()
        #        print("server_data =", server_data)

        # Check if server settings are newer
        if server_data["last_modified"] > local_last_modified:
            new_settings = server_data["settings"]

            # Compare and collect updated items
            def format_timestamp(ts):
                try:
                    t = int(ts)
                    t2000 = (
                        t - 946684800 + 7200
                    )  # 946684800 = seconds from 1970 to 2000, 7200 = GMT+2
                    time_tuple = utime.localtime(t2000)
                    return "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
                        time_tuple[0],
                        time_tuple[1],
                        time_tuple[2],
                        time_tuple[3],
                        time_tuple[4],
                        time_tuple[5],
                    )
                except Exception:
                    return str(ts)

            updated_items = "Updated settings:\n"
            for key in new_settings:
                if (
                    key not in local_settings
                    or new_settings[key] != local_settings[key]
                ):
                    if key == "last_modified":
                        old_val = local_settings.get(key, "Not set")
                        new_val = new_settings[key]
                        old_str = format_timestamp(old_val)
                        new_str = format_timestamp(new_val)
                        updated_items += f"  {key}: {old_str} -> {new_str}\n"
                    else:
                        updated_items += f"  {key}: {local_settings.get(key, 'Not set')} -> {new_settings[key]}\n"

            # Print updated items inside a box
            print_in_box(updated_items.strip())

            # Update local settings by writing to the file
            new_settings["last_modified"] = server_data["last_modified"]
            with open(LOCAL_SETTINGS_FILE, "w") as f:
                ujson.dump(new_settings, f)

            # Print the success message inside a box
            print_in_box("Settings file updated")
            # usfs_loop = usfs_loop + 1

        else:
            #            print_in_box("Settings are up to date from " + local_last_modified_date)
            if usfs_loop in (-8, 0, 5):
                # print("usfs_loop is", usfs_loop, end=" : ")
                print_in_box("Settings are up to date from " + local_last_modified_date)
        ##                print("usfs_loop is", usfs_loop)
        ##                if usfs_loop == 15:
        #                    usfs_loop = -1
        # Print the no-update message inside a box
        # print_in_box("Settings are up to date from " + local_last_modified_date)
        usfs_loop = usfs_loop + 1
        if usfs_loop > 4:
            usfs_loop = 0

    except OSError as e:
        print("|" + "¯" * 63 + "|")
        print("| Network error while updating settings:", str(e) + "  |")
        print("| Using previously updated local 'fermenter_settings.ujson' file |")
        print(
            "|  u_s_f_s.py row 137 - previous update was at",
            local_last_modified_date,
            " " * 18 + "|",
        )
        print("|" + "_" * 63 + "|")
    except ValueError as e:
        print("Error parsing JSON:", str(e))
    except Exception as e:
        print("Unexpected error while updating settings:", str(e))
    finally:
        if "response" in locals():
            response.close()


#    print("Updated OTHER_SETTINGS:", OTHER_SETTINGS)
#    print()

# ===============================================================================#

# update_settings_from_server()
# print("====== 'update_settings_from_server.py' loaded ======")
# print()

print("G ==========   END IMPORT 'update_settings_from_server.py'========== G")
