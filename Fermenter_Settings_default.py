# Constants --------------------------------------------------

# Wort temperature setting - °C
WT_s = 23.4  # 20.5
## Number of temperature reading cycles to averager
HISTORY_LENGTH = 12

# Sensor ROMs -------------------------------------------------
## Define the ROM addresses for each sensor
SENSOR_1_ROM = "28ff67c602170317"
SENSOR_2_ROM = "28a647b40a0000bd"
SENSOR_3_ROM = "289cfab20a000035"

# Control Settings

# Cold settings (OT < WT_s ())
##  'Outside Temperature' is less than 'Wort Tempereture setting'
###   Time in minutes
CON_p_cold = 1.00  # 2.00 # Cool ON period
COF_d_cold = 1.00  # 2.25 # Cool OFF delay
HON_p_cold = 1.00  # 2.75 # Heat ON period
HOF_d_cold = 1.00  #     # Heat OFF delay
###   Temperature in °C
CON_os_cold = 0.500  #   # Cool ON offset
COF_os_cold = 0.500  #   # Cool OFF offset
HON_os_cold = -0.500  #  # Heat ON offset
HOF_os_cold = -0.500  #  # Heat OFF offset
WT_so_cold = -0.020  #   # Wort Tempeture Setting offset

# Warm settings (OT > WT_s)
##  'Outside Temperature' is more than 'Wort Tempereture setting'
###   Time in minutes
CON_p_warm = 1.00  # 3.75
COF_d_warm = 1.00  # 1.0
HON_p_warm = 1.00
HOF_d_warm = 1.00  # 1.0
###   Temperature in °C
CON_os_warm = 0.050
COF_os_warm = 0.500
HON_os_warm = -0.500
HOF_os_warm = -0.500
WT_so_warm = -0.020


# Definitions

#  C / H ON_p_ cold / warm
##   ON period for cooler or heater, in minutes
# C / H OF_d_ cold / warm
##   OFF delay, cooler or heater off while chamber temperature stabilises
# C / H ON_os_ cold / warm
##

## Wort (Fermenting) Temperature setting - °C
# WT_s = 21
##
