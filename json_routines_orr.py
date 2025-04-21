print("========== START OF json_routines.py ========== 7")

from debug_config import debug_4_print

debug_4_print("=== 'json_routines.py' import start === " + ">" * 40)

import json

# import Fermenter_Settings


# ====================================================================================#
def get_default_settings():
    debug_4_print(
        "=== 'json_routines.py - get_default_settings() start === " + ">" * 25
    )
    return {
        "WT_s": Fermenter_Settings.WT_s,
        "HISTORY_LENGTH": Fermenter_Settings.HISTORY_LENGTH,
        "SENSOR_1_ROM": Fermenter_Settings.SENSOR_1_ROM,
        "SENSOR_2_ROM": Fermenter_Settings.SENSOR_2_ROM,
        "SENSOR_3_ROM": Fermenter_Settings.SENSOR_3_ROM,
        "CON_p_cold": Fermenter_Settings.CON_p_cold,
        "COF_d_cold": Fermenter_Settings.COF_d_cold,
        "HON_p_cold": Fermenter_Settings.HON_p_cold,
        "HOF_d_cold": Fermenter_Settings.HOF_d_cold,
        "CON_os_cold": Fermenter_Settings.CON_os_cold,
        "COF_os_cold": Fermenter_Settings.COF_os_cold,
        "HON_os_cold": Fermenter_Settings.HON_os_cold,
        "HOF_os_cold": Fermenter_Settings.HOF_os_cold,
        "WT_so_cold": Fermenter_Settings.WT_so_cold,
        "CON_p_warm": Fermenter_Settings.CON_p_warm,
        "COF_d_warm": Fermenter_Settings.COF_d_warm,
        "HON_p_warm": Fermenter_Settings.HON_p_warm,
        "HOF_d_warm": Fermenter_Settings.HOF_d_warm,
        "CON_os_warm": Fermenter_Settings.CON_os_warm,
        "COF_os_warm": Fermenter_Settings.COF_os_warm,
        "HON_os_warm": Fermenter_Settings.HON_os_warm,
        "HOF_os_warm": Fermenter_Settings.HOF_os_warm,
        "WT_so_warm": Fermenter_Settings.WT_so_warm,
    }
    debug_4_print(
        "=== 'json_routines.py - get_default_settings() end   === " + "<" * 25
    )


# ====================================================================================#
def create_settings_json():
    debug_4_print(
        "=== 'json_routines.py - create_settings_json() start === " + ">" * 25
    )
    settings = get_default_settings()
    with open("fermenter_settings.ujson", "w") as f:
        json.dump(settings, f)
    debug_4_print(
        "=== 'json_routines.py - create_settings_json() end   === " + "<" * 25
    )


# ====================================================================================#
def read_settings_json():
    debug_4_print("=== 'json_routines.py - read_settings_json() start === " + ">" * 25)
    try:
        with open("fermenter_settings.ujson", "r") as f:
            debug_4_print(
                "=== 'json_routines.py - read_settings_json() end === " + "<" * 25
            )
            return json.load(f)
            debug_4_print(
                "=== 'json_routines.py - read_settings_json() end === " + "<" * 25
            )
    except:
        # If file doesn't exist or is corrupted, create a new one
        create_settings_json()
        debug_4_print(
            "=== 'json_routines.py - read_settings_json() end === " + "<" * 25
        )
        return read_settings_json()
    debug_4_print("=== 'json_routines.py - read_settings_json() end === " + "<" * 25)


# ====================================================================================#
def update_setting(key, value):
    debug_4_print("=== 'json_routines.py - update_settings() start === " + ">" * 25)
    settings = read_settings_json()
    settings[key] = value
    with open("fermenter_settings.ujson", "w") as f:
        json.dump(settings, f)
    debug_4_print("=== 'json_routines.py - update_settings() end   === " + "<" * 25)


# ====================================================================================#
def fetch_sensor_1_rom():
    debug_4_print("=== 'json_routines.py - fetch_sensor_1_rom() start === " + ">" * 25)
    settings = read_settings_json()
    if settings:
        sensor_1_rom = settings.get("SENSOR_1_ROM")
        if sensor_1_rom:
            print("SENSOR_1_ROM:", sensor_1_rom)
        else:
            print("SENSOR_1_ROM not found in the JSON file.")
    else:
        print("Failed to load settings from JSON file.")
    debug_4_print("=== 'json_routines.py - fetch_sensor_1_rom() end   === " + "<" * 25)


# ====================================================================================#
def fetch_history_length():
    debug_4_print(
        "=== 'json_routines.py - fetch_history_length() start === " + ">" * 25
    )
    global history_length

    settings = read_settings_json()
    if settings:
        history_length = settings.get("HISTORY_LENGTH")
        if history_length:
            print("HISTORY_LENGTH:", history_length)
        else:
            print("HISTORY_LENGTH not found in the JSON file.")
    else:
        print("Failed to load settings from JSON file.")
    debug_4_print(
        "=== 'json_routines.py - fetch_history_length() end   === " + "<" * 25
    )


# ====================================================================================#
# print("====== 'json_routines.py' loaded ======")
# print()
# get_default_settings()
# read_settings_json()
# fetch_sensor_1_rom()
# fetch_history_length()

debug_4_print("=== 'json_routines.py' import end   === " + "<" * 40)

print("========== END OF json_routines.py ========== 7")
