# te__relay_C_O_H__db__routes.py
# temperature and database routines

print("H ========== START IMPORT 'te__relay_C_O_H__db__routes.py' ========= H")

import settings
import sensors
import history
from sensor_display import display_sensor_table
from control_routine import run_control_cycle

# ===============================================================================#

global tr_1_avg, tr_1_act, tr_2_avg, tr_2_act, tr_3_avg, tr_3_act
tr_1_avg = tr_1_act = tr_2_avg = tr_2_act = tr_3_avg = tr_3_act = None


# ===============================================================================#
# --------------------------------------------------------------------------
def read_temps():
    return sensors.read_temps()


# ===============================================================================#
# --------------------------------------------------------------------------
current_mode = None
cycles_in_mode = 0
cycles_in_idle = 0

# ===============================================================================#

# ===============================================================================#


def get_tr_temps():
    """Read sensors, update globals, display data, and run control route."""
    global tr_1_avg, tr_1_act, tr_2_avg, tr_2_act, tr_3_avg, tr_3_act
    # Fetch sensor ROMs
    other_settings = settings.other_settings()
    sensor_1_rom = other_settings.get("SENSOR_1_ROM")
    sensor_2_rom = other_settings.get("SENSOR_2_ROM")
    sensor_3_rom = other_settings.get("SENSOR_3_ROM")
    # Read and process temperatures
    temps = sensors.read_temps()
    history.history.update(temps)
    avg_temps = history.history.averages()
    # Display sensor table
    labels = [
        ("Sensor 1 WT", sensor_1_rom),
        ("Sensor 2 CT", sensor_2_rom),
        ("Sensor 3 OT", sensor_3_rom),
    ]
    display_sensor_table(temps, avg_temps, labels)
    # Update globals
    if sensor_1_rom in temps:
        tr_1_act = temps[sensor_1_rom]
        tr_1_avg = avg_temps.get(sensor_1_rom, tr_1_act)
    if sensor_2_rom in temps:
        tr_2_act = temps[sensor_2_rom]
        tr_2_avg = avg_temps.get(sensor_2_rom, tr_2_act)
    if sensor_3_rom in temps:
        tr_3_act = temps[sensor_3_rom]
        tr_3_avg = avg_temps.get(sensor_3_rom, tr_3_act)
    # Invoke refactored control cycle
    global current_mode, cycles_in_mode, cycles_in_idle
    current_mode, cycles_in_mode, cycles_in_idle = run_control_cycle(
        tr_1_avg,
        tr_1_act,
        tr_2_avg,
        tr_2_act,
        tr_3_avg,
        tr_3_act,
        current_mode,
        cycles_in_mode,
        cycles_in_idle,
    )


# ===============================================================================#

print("H ==========   END IMPORT 'te__relay_C_O_H__db__routes.py' ========= H")
