"""
control_routine.py
Encapsulates one fermentation control cycle: settings, control logic, displays, and server send.
"""

import time
import settings
import control
import server

from setting_display import display_wort_setting
from status_display import display_phase, display_env_and_limits
from data_formatter import display_db_data
from mode_display import display_mode_char
from control_helpers import get_phase_text, get_db_data


def run_control_cycle(
    tr1_avg,
    tr1_act,
    tr2_avg,
    tr2_act,
    tr3_avg,
    tr3_act,
    current_mode,
    cycles_in_mode,
    cycles_in_idle,
):
    """
    Runs one cycle: displays setpoint, executes control, updates displays, sends payload.
    Returns updated (current_mode, cycles_in_mode, cycles_in_idle).
    """
    # Temperatures
    w_t = tr1_avg
    c_t = tr2_avg
    o_t = tr3_avg
    wt_a = tr1_act
    ct_a = tr2_act
    ot_a = tr3_act

    # Wort setpoint
    wt_s = settings.other_settings().get("WT_s")
    w_t_s = wt_s
    params = control.calculate_parameters(o_t)
    w_t_s_c = wt_s + params.get("WT_so", 0)

    # Display wort setting
    display_wort_setting(w_t_s, w_t, c_t)

    # Execute relay control
    current_mode, cycles_in_mode, cycles_in_idle = control.temp_relay_control(
        w_t, c_t, o_t, current_mode, cycles_in_mode, cycles_in_idle
    )

    # Phase and environment displays
    phase_text = get_phase_text(current_mode, cycles_in_mode, cycles_in_idle, params)
    display_phase(phase_text)
    display_env_and_limits(w_t, c_t, o_t, params)

    # Prepare and send payload
    db_data = get_db_data(
        w_t,
        c_t,
        o_t,
        w_t_s,
        w_t_s_c,
        params["cool_on"],
        params["cool_off"],
        params["heat_on"],
        params["heat_off"],
        round(control.cycles_to_minutes(params["cool_on_period"]), 2),
        round(control.cycles_to_minutes(params["cool_off_delay"]), 2),
        round(control.cycles_to_minutes(params["heat_on_period"]), 2),
        round(control.cycles_to_minutes(params["heat_off_delay"]), 2),
        control.mode_to_string(current_mode),
        current_mode,
        cycles_in_mode,
        wt_a,
        ct_a,
        ot_a,
    )
    display_db_data(db_data)
    server.send_2_server(db_data)

    # Update 7-seg
    display_mode_char(current_mode)

    return current_mode, cycles_in_mode, cycles_in_idle
