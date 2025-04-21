"""
DS18B20 sensor reading + calibration offsets.
"""

import machine
import onewire
import ds18x20
import time
import settings

# Default pin for DS18B20 data line (GPIO4 on NodeMCU)
DEFAULT_PIN = 4


def read_temps(pin_num=DEFAULT_PIN):
    """
    Read raw temperatures from DS18B20 sensors, apply per-sensor offsets, and return a dict mapping ROM strings to temps.
    """
    other_settings = settings.other_settings()
    sensor_1_rom = other_settings.get("SENSOR_1_ROM")
    sensor_2_rom = other_settings.get("SENSOR_2_ROM")
    sensor_3_rom = other_settings.get("SENSOR_3_ROM")

    # Initialize one-wire bus and DS18X20 driver
    dat = machine.Pin(pin_num)
    ds = ds18x20.DS18X20(onewire.OneWire(dat))
    roms = ds.scan()

    # Trigger conversion and wait
    ds.convert_temp()
    time.sleep_ms(750)

    temps = {}
    for rom in roms:
        rom_str = "".join("{:02x}".format(b) for b in rom)
        temp = ds.read_temp(rom)
        # Apply calibration offsets
        if rom_str == sensor_1_rom:
            temp += 0.250 + 0.0625
        if rom_str == sensor_2_rom:
            temp += 0
        if rom_str == sensor_3_rom:
            temp += -0.25
        temps[rom_str] = temp
    return temps
