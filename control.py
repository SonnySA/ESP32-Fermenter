"""
Control logic for fermentation: mode enum, parameter calculations, and relay control.
"""

import math
import time
import settings
import relay_drive


class Mode:
    COOLING = 1
    COOL_REST = 2
    HEATING = 3
    HEAT_REST = 4
    IDLE = 0


def minutes_to_cycles(minutes):
    """Convert minutes to 15s cycles."""
    return math.ceil(minutes * 60 / 15)


def cycles_to_minutes(cycles):
    """Convert 15s cycles back to minutes."""
    return cycles * 15 / 60


def mode_to_string(mode):
    if mode == Mode.COOLING:
        return "COOLING"
    elif mode == Mode.COOL_REST:
        return "COOL REST"
    elif mode == Mode.HEATING:
        return "HEATING"
    elif mode == Mode.HEAT_REST:
        return "HEAT REST"
    elif mode == Mode.IDLE:
        return "IDLE"
    else:
        return "UNKNOWN"


def calculate_parameters(outside_temp):
    wt_s = settings.get("WT_s")
    cold_settings = settings.cold_settings()
    warm_settings = settings.warm_settings()
    use_settings = cold_settings if outside_temp <= wt_s else warm_settings

    return {
        "cool_on": wt_s + use_settings["CON_os"],
        "cool_off": wt_s + use_settings["COF_os"],
        "heat_on": wt_s + use_settings["HON_os"],
        "heat_off": wt_s + use_settings["HOF_os"],
        "HON_p": use_settings["HON_p"],
        "HOF_d": use_settings["HOF_d"],
        "CON_p": use_settings["CON_p"],
        "COF_d": use_settings["COF_d"],
        "WT_so": use_settings["WT_so"],
        "cool_on_period": use_settings["CON_p"],
        "cool_off_delay": use_settings["COF_d"],
        "heat_on_period": use_settings["HON_p"],
        "heat_off_delay": use_settings["HOF_d"],
    }


def temp_relay_control(
    wort_temp, chamber_temp, outside_temp, current_mode, cycles_in_mode, cycles_in_idle
):
    """
    Determine new mode based on temperatures and drive relays accordingly.
    Returns (new_mode, updated_cycles_in_mode, updated_cycles_in_idle).
    """
    wt_s = settings.get("WT_s")
    params = calculate_parameters(outside_temp)
    WT_sc = wt_s + params["WT_so"]

    # Mode transition logic
    if current_mode == Mode.HEATING:
        if cycles_in_mode >= params["HON_p"] or wort_temp > params["heat_off"]:
            new_mode = Mode.HEAT_REST
            cycles_in_mode = 0
        else:
            new_mode = Mode.HEATING
            cycles_in_mode += 1
    elif current_mode == Mode.HEAT_REST:
        if cycles_in_mode >= params["HOF_d"]:
            if wort_temp < params["heat_on"] and chamber_temp < WT_sc:
                new_mode = Mode.HEATING
                cycles_in_mode = 0
            else:
                new_mode = Mode.IDLE
                cycles_in_mode = 0
                cycles_in_idle = 0
        else:
            new_mode = Mode.HEAT_REST
            cycles_in_mode += 1
    elif current_mode == Mode.COOLING:
        if cycles_in_mode >= params["CON_p"] or (
            wort_temp < params["cool_off"] - 0.1 and chamber_temp < WT_sc + 0.5
        ):
            new_mode = Mode.COOL_REST
            cycles_in_mode = 0
        else:
            new_mode = Mode.COOLING
            cycles_in_mode += 1
    elif current_mode == Mode.COOL_REST:
        if cycles_in_mode >= params["COF_d"]:
            if wort_temp > params["cool_on"] and chamber_temp > WT_sc:
                new_mode = Mode.COOLING
                cycles_in_mode = 0
            else:
                new_mode = Mode.IDLE
                cycles_in_mode = 0
                cycles_in_idle = 0
        else:
            new_mode = Mode.COOL_REST
            cycles_in_mode += 1
    elif current_mode == Mode.IDLE:
        if (wort_temp > params["cool_on"] and chamber_temp > params["cool_off"]) or (
            wort_temp > WT_sc and chamber_temp > WT_sc + 0.5
        ):
            new_mode = Mode.COOLING
            cycles_in_mode = 0
            cycles_in_idle = 0
        elif (
            (wort_temp < params["heat_on"] and chamber_temp < params["heat_off"])
            or (wort_temp < WT_sc and chamber_temp < WT_sc - 0.5)
            or (wort_temp < WT_sc - 0.5 and chamber_temp < WT_sc + 0.5)
        ):
            new_mode = Mode.HEATING
            if chamber_temp > WT_sc + 1:
                new_mode = Mode.IDLE
            cycles_in_mode = 0
            cycles_in_idle = 0
        else:
            new_mode = Mode.IDLE
            cycles_in_idle += 1
    else:
        new_mode = Mode.IDLE

    # Apply relays
    if new_mode == Mode.COOLING:
        relay_drive.Cool_ON()
        relay_drive.Heat_OFF()
        relay_status = "RELAY-COOL: ACTIVATED, Relay-heat: deactivated"
    elif new_mode == Mode.HEATING:
        relay_drive.Heat_ON()
        relay_drive.Cool_OFF()
        relay_status = "RELAY-HEAT: ACTIVATED, Relay-cool: deactivated"
    else:
        relay_drive.Cool_OFF()
        relay_drive.Heat_OFF()
        relay_status = "Relay-heat: deactivated, Relay-cool: deactivated"

    # Display relay status
    print("waiting ......", end="")
    time.sleep(0.02)
    print("\r┌" + "─" * len(relay_status) + "┐")
    print("│" + relay_status + "│")
    print("└" + "─" * len(relay_status) + "┘")

    return new_mode, cycles_in_mode, cycles_in_idle
