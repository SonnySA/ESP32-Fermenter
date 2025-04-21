"""
data_formatter.py
Module to format and display database payload boxes.
"""

from display import wait, box_sep, box_bottom


def display_db_data(db_data):
    """Builds and prints a boxed view of the db_data payload."""
    # Extract values
    w_t = db_data.get("w_t")
    c_t = db_data.get("c_t")
    o_t = db_data.get("o_t")
    w_t_s = db_data.get("w_t_s")
    w_t_s_c = db_data.get("w_t_s_c")
    c_on_s = db_data.get("c_on_s")
    c_off_s = db_data.get("c_off_s")
    h_on_s = db_data.get("h_on_s")
    h_off_s = db_data.get("h_off_s")
    c_on_p = db_data.get("c_on_p")
    c_off_d = db_data.get("c_off_d")
    h_on_p = db_data.get("h_on_p")
    h_off_d = db_data.get("h_off_d")
    m_na = db_data.get("m_na")
    m_nu = db_data.get("m_nu")
    m_cy = db_data.get("m_cy")

    # Build formatted lines
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

    lines = [line1, line2, line3, line4]
    max_width = max(len(l) for l in lines)
    box_width = max_width + 4  # 2 spaces margin each side

    # Print boxed payload
    wait()
    box_sep(box_width)
    for l in lines:
        print("│  {:<{width}}  │".format(l, width=max_width))
    box_bottom(box_width)
