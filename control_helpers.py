"""
control_helpers.py
Helper routines to generate phase text and database payloads for fermentation control.
"""

import control


def get_phase_text(current_mode, cycles_in_mode, cycles_in_idle, params):
    """Return status text based on mode, cycles, and parameters."""
    if current_mode == control.Mode.COOLING:
        total = control.cycles_to_minutes(params["CON_p"])
        rem = control.cycles_to_minutes(params["CON_p"] - cycles_in_mode)
        return f"Cooling ON period (CON_p): {total:.2f} minutes | Time remaining: {rem:.2f}/{total:.2f} minutes"
    elif current_mode == control.Mode.COOL_REST:
        total = control.cycles_to_minutes(params["COF_d"])
        rem = control.cycles_to_minutes(params["COF_d"] - cycles_in_mode)
        return f"Cooling REST period (COF_d): {total:.2f} minutes | Time remaining: {rem:.2f}/{total:.2f} minutes"
    elif current_mode == control.Mode.HEATING:
        total = control.cycles_to_minutes(params["HON_p"])
        rem = control.cycles_to_minutes(params["HON_p"] - cycles_in_mode)
        return f"Heating ON period (HON_p): {total:.2f} minutes | Time remaining: {rem:.2f}/{total:.2f} minutes"
    elif current_mode == control.Mode.HEAT_REST:
        total = control.cycles_to_minutes(params["HOF_d"])
        rem = control.cycles_to_minutes(params["HOF_d"] - cycles_in_mode)
        return f"Heating REST period (HOF_d): {total:.2f} minutes | Time remaining: {rem:.2f}/{total:.2f} minutes"
    else:
        return f"System is IDLE | Cycles in idle: {cycles_in_idle}"


def get_db_data(
    w_t,
    c_t,
    o_t,
    w_t_s,
    w_t_s_c,
    c_on_s,
    c_off_s,
    h_on_s,
    h_off_s,
    c_on_p,
    c_off_d,
    h_on_p,
    h_off_d,
    m_na,
    m_nu,
    m_cy,
    wt_a,
    ct_a,
    ot_a,
):
    """Builds the payload dict for server transmission."""
    return {
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
