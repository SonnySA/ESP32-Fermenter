# te__relay_C_O_H__db__routes.py
# temperature and database routines

print("H ========== START IMPORT 'te__relay_C_O_H__db__routes.py' ========= H")

import time
import relay_drive
import save_clear_db
from display_drive import display_char

import d_t_routs
import settings
import sensors
import history
import control
import server

# ===============================================================================#

global tr_1_avg, tr_1_act, tr_2_avg, tr_2_act, tr_3_avg, tr_3_act
tr_1_avg = tr_1_act = tr_2_avg = tr_2_act = tr_3_avg = tr_3_act = None


# ===============================================================================#
# --------------------------------------------------------------------------
def read_temps():
    return sensors.read_temps()


# ===============================================================================#
# --------------------------------------------------------------------------
current_mode = control.Mode.IDLE
cycles_in_mode = 0
cycles_in_idle = 0

# ===============================================================================#

# ===============================================================================#


def C_O_H_rout():
    global current_mode, cycles_in_mode, cycles_in_idle, db_data, increasing

    loops = 0

    wort_temp = tr_1_avg
    chamber_temp = tr_2_avg
    outside_temp = tr_3_avg

    # Fetch WT_s from settings at the start of the function
    wt_s = settings.other_settings().get("WT_s")

    wort_temp_setting = wt_s

    params = control.calculate_parameters(outside_temp)
    WT_sc = wt_s + params["WT_so"]
    wort_temp_setting_corrected = wt_s + params["WT_so"]

    # Replace the temperature reading code with this:
    temp_values = get_temp_values()
    wort_temp = tr_1_avg
    chamber_temp = tr_2_avg
    outside_temp = tr_3_avg

    wort_temp_act = tr_1_act
    chamber_temp_act = tr_2_act
    outside_temp_act = tr_3_act

    # Calculate parameters based on outside temperature
    params = control.calculate_parameters(outside_temp)

    CON = params["cool_on"]
    COF = params["cool_off"]
    HON = params["heat_on"]
    HOF = params["heat_off"]

    cool_on_setting = params["cool_on"]
    cool_off_setting = params["cool_off"]
    heat_on_setting = params["heat_on"]
    heat_off_setting = params["heat_off"]

    cool_on_period = round(control.cycles_to_minutes(params["cool_on_period"]), 2)
    cool_off_delay = round(control.cycles_to_minutes(params["cool_off_delay"]), 2)
    heat_on_period = round(control.cycles_to_minutes(params["heat_on_period"]), 2)
    heat_off_delay = round(control.cycles_to_minutes(params["heat_off_delay"]), 2)

    print("waiting ....", end="")
    time.sleep(0.02)  # Delay for a short moment (10 milliseconds)
    print("\r┌" + "─" * 76 + "┐")
    print(
        "│Wort Temperature Setting = {:.3f}, "
        "Wort Temp = {:.3f}, Chamber Temp = {:.3f}".format(
            wort_temp_setting, wort_temp, chamber_temp
        )
        + "│"
    )
    print("└" + "─" * 76 + "┘")

    # Call the temperature and relay control function
    current_mode, cycles_in_mode, cycles_in_idle = control.temp_relay_control(
        wort_temp,
        chamber_temp,
        outside_temp,
        current_mode,
        cycles_in_mode,
        cycles_in_idle,
    )

    # Print the current state and time information
    # print(f"Mode: {mode_to_string(current_mode)}")

    # Calculate and print the relevant time based on the current mode
    if current_mode == control.Mode.COOLING:
        total_minutes = control.cycles_to_minutes(params["CON_p"])
        minutes_remaining = control.cycles_to_minutes(params["CON_p"] - cycles_in_mode)
        text = (
            "Cooling ON period (CON_p): {:.2f} minutes | "
            "Time remaining: {:.2f}/{:.2f} minutes"
        ).format(total_minutes, minutes_remaining, total_minutes)
    elif current_mode == control.Mode.COOL_REST:
        total_minutes = control.cycles_to_minutes(params["COF_d"])
        minutes_remaining = control.cycles_to_minutes(params["COF_d"] - cycles_in_mode)
        text = (
            "Cooling REST period (COF_d): {:.2f} minutes | "
            "Time remaining: {:.2f}/{:.2f} minutes"
        ).format(total_minutes, minutes_remaining, total_minutes)
    elif current_mode == control.Mode.HEATING:
        total_minutes = control.cycles_to_minutes(params["HON_p"])
        minutes_remaining = control.cycles_to_minutes(params["HON_p"] - cycles_in_mode)
        text = (
            "Heating ON period (HON_p): {:.2f} minutes | "
            "Time remaining: {:.2f}/{:.2f} minutes"
        ).format(total_minutes, minutes_remaining, total_minutes)
    elif current_mode == control.Mode.HEAT_REST:
        total_minutes = control.cycles_to_minutes(params["HOF_d"])
        minutes_remaining = control.cycles_to_minutes(params["HOF_d"] - cycles_in_mode)
        text = (
            "Heating REST period (HOF_d): {:.2f} minutes | "
            "Time remaining: {:.2f}/{:.2f} minutes"
        ).format(total_minutes, minutes_remaining, total_minutes)
    elif current_mode == control.Mode.IDLE:
        text = "System is IDLE | Cycles in idle: {}".format(cycles_in_idle)

    # Print the boxed text
    box_width = len(text) + 2  # Adding 2 to account for box borders
    print("waiting ....", end="")
    time.sleep(0.02)  # Delay for a short moment (10 milliseconds)
    print("\r┌" + "─" * box_width + "┐")
    print("│ " + text + " │")
    print("└" + "─" * box_width + "┘")

    print("waiting .....", end="")
    time.sleep(0.02)  # Delay for a short moment (10 milliseconds)
    print("\r┌" + "─" * 72 + "┐")  # Print a separator line for readability
    print(
        "│Temperatures - Wort: {:.2f}, Chamber: {:.2f}, Outside: {:.2f}".format(
            wort_temp, chamber_temp, outside_temp
        )
        + " " * 14
        + "│"
    )
    print(
        "│Temperature Limits - CON: {:.3f}, COF: {:.3f}, HON: {:.3f}, HOF: {:.3f}".format(
            params["cool_on"], params["cool_off"], params["heat_on"], params["heat_off"]
        )
        + " " * 1
        + "│"
    )
    print("└" + "─" * 72 + "┘")  # Print a separator line for readability 'Alt 0175'

    mode_name = control.mode_to_string(current_mode)
    mode_number = current_mode
    mode_cycles = cycles_in_mode

    # data to be sent to server
    w_t = wort_temp
    c_t = chamber_temp
    o_t = outside_temp
    w_t_s = wort_temp_setting
    w_t_s_c = wort_temp_setting_corrected
    c_on_s = cool_on_setting
    c_off_s = cool_off_setting
    c_on_p = cool_on_period
    c_off_d = cool_off_delay
    h_on_s = heat_on_setting
    h_off_s = heat_off_setting
    h_on_p = heat_on_period
    h_off_d = heat_off_delay
    m_na = mode_name
    m_nu = mode_number
    m_cy = mode_cycles

    wt_a = wort_temp_act  # = tr_1_act
    ct_a = chamber_temp_act  # = tr_2_act
    ot_a = outside_temp_act  # = tr_3_act

    if m_na == "IDLE":
        #        print(m_na)
        #        m_cy = cycles_in_idle * 4
        m_cy = cycles_in_idle * 1
    # call_break.c_break()
    if m_na == "COOLING" and cycles_in_mode == 0:
        # c_on_s = wort_temp_setting_corrected
        w_t_s = c_on_s

    if m_na == "COOL REST" and cycles_in_mode == 0:
        # c_off_s = wort_temp_setting_corrected
        w_t_s = c_off_s

    if m_na == "HEATING" and cycles_in_mode == 0:
        # h_on_s = wort_temp_setting_corrected
        w_t_s = h_on_s

    if m_na == "HEAT REST" and cycles_in_mode == 0:
        # h_off_s = wort_temp_setting_corrected
        w_t_s = h_off_s

    # Create a dictionary with only the data we want to send - 16 items
    db_data = {
        "w_t": w_t,
        "c_t": c_t,
        "o_t": o_t,
        "w_t_s": w_t_s,
        "w_t_s_c": w_t_s_c,
        "h_on_s": h_on_s,
        "h_off_s": h_off_s,
        "h_on_p": h_on_p,
        "h_off_d": h_off_d,
        "c_on_s": c_on_s,
        "c_off_s": c_off_s,
        "c_on_p": c_on_p,
        "c_off_d": c_off_d,
        "m_na": m_na,
        "m_nu": m_nu,
        "m_cy": m_cy,
        "wt_a": wt_a,
        "ct_a": ct_a,
        "ot_a": ot_a,
    }

    time.sleep(0.01)  # Delay for a short moment (10 milliseconds)

    # Prepare the data strings
    line1 = (
        "w_t   : {:.3f}, c_t    : {:.3f}, o_t   : {:.3f}, "
        "w_t_s  : {:.3f}, w_t_s_c: {:.3f}"
    ).format(w_t, c_t, o_t, w_t_s, w_t_s_c)

    line2 = (
        "c_on_s: {:.3f}, c_off_s: {:.3f}, " "h_on_s: {:.3f}, h_off_s: {:.3f}"
    ).format(c_on_s, c_off_s, h_on_s, h_off_s)

    line3 = (
        "c_on_p: {:.3f},  c_off_d: {:.3f},  " "h_on_p: {:.3f},  h_off_d: {:.3f}"
    ).format(c_on_p, c_off_d, h_on_p, h_off_d)

    line4 = "m_na  : {},   m_nu: {}, m_cy: {}".format(m_na, m_nu, m_cy)

    # Calculate the maximum width needed
    max_width = max(
        len(line1),
        len(line2),
        len(line3),
        len(line4),
        len("db data to be sent to Server:"),
    )
    box_width = max_width + 4  # Add 4 for padding (2 on each side)

    # Print the box
    print("┌ db data to be sent to Server:" + "─" * (box_width - 32) + "┐")
    print("│ {:<{width}} │".format(line1, width=box_width - 4))
    print("│ {:<{width}} │".format(line2, width=box_width - 4))
    print("│ {:<{width}} │".format(line3, width=box_width - 4))
    print("│ {:<{width}} │".format(line4, width=box_width - 4))
    print("└" + "─" * (box_width - 2) + "┘")

    server.send_2_server(db_data)

    # Display Drive addition

    # Example value for m_nu
    #    m_nu = 2  # This would typically be set or passed into the function

    # Dictionary to map m_nu values to corresponding characters
    char_map = {0: "O", 1: "C", 2: "c", 3: "H", 4: "h"}

    # Get the corresponding character for the current m_nu value
    char = char_map.get(m_nu)

    if char is not None:
        # Call the display_char function with the corresponding character
        display_char(char)
    else:
        # Handle the case where m_nu is not in the expected range
        print("Invalid value for m_nu")


# ===============================================================================#


def get_tr_temps():
    global tr_1_avg, tr_1_act, tr_2_avg, tr_2_act, tr_3_avg, tr_3_act, c_o_h

    # Fetch sensor ROMs from settings at the start of the function
    other_settings = settings.other_settings()
    sensor_1_rom = other_settings.get("SENSOR_1_ROM")
    sensor_2_rom = other_settings.get("SENSOR_2_ROM")
    sensor_3_rom = other_settings.get("SENSOR_3_ROM")

    temps = sensors.read_temps()  # Temperatures are already corrected here
    history.history.update(temps)
    avg_temps = history.history.averages()

    tr_data = {
        "tr_1_avg": None,
        "tr_2_avg": None,
        "tr_3_avg": None,
        "tr_1_act": None,
        "tr_2_act": None,
        "tr_3_act": None,
        "c_o_h": None,
    }

    print("waiting ....", end="")
    time.sleep(0.02)  # Delay for a short moment (10 milliseconds)
    print("\r┌" + "─" * 41 + "┐")
    print("│Sensor      | Current Temp | Average Temp│")
    print("│────────────|──────────────|─────────────│")

    # Sensor 1
    if sensor_1_rom in temps:
        current_temp = temps[sensor_1_rom]
        avg_temp = avg_temps.get(sensor_1_rom, current_temp)
        tr_data["tr_1_avg"] = tr_1_avg = avg_temp
        tr_data["tr_1_act"] = tr_1_act = current_temp
        print(f"│Sensor 1 WT | {current_temp:9.3f}    |  {avg_temp:8.3f}   │")

    # Sensor 2
    if sensor_2_rom in temps:
        current_temp = temps[sensor_2_rom]
        avg_temp = avg_temps.get(sensor_2_rom, current_temp)
        tr_data["tr_2_avg"] = tr_2_avg = avg_temp
        tr_data["tr_2_act"] = tr_2_act = current_temp
        print(f"│Sensor 2 CT | {current_temp:9.3f}    |  {avg_temp:8.3f}   │")

    # Sensor 3
    if sensor_3_rom in temps:
        current_temp = temps[sensor_3_rom]
        avg_temp = avg_temps.get(sensor_3_rom, current_temp)
        tr_data["tr_3_avg"] = tr_3_avg = avg_temp
        tr_data["tr_3_act"] = tr_3_act = current_temp
        print(f"│Sensor 3 OT | {current_temp:9.3f}    |  {avg_temp:8.3f}   │")
        print("└" + "─" * 41 + "┘")

    C_O_H_rout()


# ===============================================================================#


def get_temp_values():

    return {
        "tr_1_avg": tr_1_avg,
        "tr_1_act": tr_1_act,
        "tr_2_avg": tr_2_avg,
        "tr_2_act": tr_2_act,
        "tr_3_avg": tr_3_avg,
        "tr_3_act": tr_3_act,
    }


print("H ==========   END IMPORT 'te__relay_C_O_H__db__routes.py' ========= H")
