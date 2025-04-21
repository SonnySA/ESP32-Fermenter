import ujson

import call_break

print(" @ 'Fermenter_Settings.py' row 6  ---  IS THIS NEEDED")
call_break.c_break()

"""
#=======================================================================#

#from load_local_settings import COLD_SETTINGS, WARM_SETTINGS, OTHER_SETTINGS, load_local_settings
from update_settings_from_server import COLD_SETTINGS, WARM_SETTINGS, OTHER_SETTINGS, load_local_settings

def get_local_settings():
    global CON_p_cold, COF_d_cold, HON_p_cold, HOF_d_cold
    global CON_os_cold, COF_os_cold, HON_os_cold, HOF_os_cold, WT_so_cold
    global CON_p_warm, COF_d_warm, HON_p_warm, HOF_d_warm, CON_os_warm
    global COF_os_warm, HON_os_warm, HOF_os_warm, WT_so_warm
    global WT_s, history_length, last_modified, HISTORY_LENGTH
    global SENSOR_1_ROM, SENSOR_2_ROM, SENSOR_3_ROM


    # At the beginning of your script or where you need the settings
    ALL_SETTINGS, COLD_SETTINGS, WARM_SETTINGS, OTHER_SETTINGS = load_local_settings()

    # Load the latest settings before using them
#    load_local_settings()

    #Access the COLD_SETTINGS
    CON_p_cold = COLD_SETTINGS.get('CON_p')
    COF_d_cold = COLD_SETTINGS.get('COF_d')
    HON_p_cold = COLD_SETTINGS.get('HON_p')
    HOF_d_cold = COLD_SETTINGS.get('HOF_d')
    CON_os_cold = COLD_SETTINGS.get('CON_os')
    COF_os_cold = COLD_SETTINGS.get('COF_os')
    HON_os_cold = COLD_SETTINGS.get('HON_os')
    HOF_os_cold = COLD_SETTINGS.get('HOF_os')
    WT_so_cold = COLD_SETTINGS.get('WT_so')

    #Access the WARM_SETTINGS
    CON_p_warm = WARM_SETTINGS.get('CON_p')
    COF_d_warm = WARM_SETTINGS.get('COF_d')
    HON_p_warm = WARM_SETTINGS.get('HON_p')
    HOF_d_warm = WARM_SETTINGS.get('HOF_d')
    CON_os_warm = WARM_SETTINGS.get('CON_os')
    COF_os_warm = WARM_SETTINGS.get('COF_os')
    HON_os_warm = WARM_SETTINGS.get('HON_os')
    HOF_os_warm = WARM_SETTINGS.get('HOF_os')
    WT_so_warm = WARM_SETTINGS.get('WT_so')

    # Access the OTHER_SETTINGS
    WT_s = OTHER_SETTINGS.get('WT_s')
    history_length = OTHER_SETTINGS.get('HISTORY_LENGTH')
    HISTORY_LENGTH = OTHER_SETTINGS.get('HISTORY_LENGTH')
    last_modified = OTHER_SETTINGS.get('last_modified')
    SENSOR_1_ROM = OTHER_SETTINGS.get('SENSOR_1_ROM')
    SENSOR_2_ROM = OTHER_SETTINGS.get('SENSOR_2_ROM')
    SENSOR_3_ROM = OTHER_SETTINGS.get('SENSOR_3_ROM')
"""

"""
def do_something_else():
    
    print("=" * 63)
    print("*** Starting 'use_local_settings_1.py  do_something_else() ***")
    
#    CON_p_warm = WARM_SETTINGS.get('CON_p')
    
#    print("%" * 10)
#    print("Started to 'do_something_else()' - will print some 'OTHER and WARM _SETTINGS'")
#    print("this is global from 'do_something' - 'history_length 'is :", history_length)
    print("'CON_p_warm' is :", CON_p_warm)
#    print("%" * 10)
    print("last_modified:", last_modified)
#    print()
    print("In 'do_something_else()' === Other Settings WT_s:", WT_s)
#    print()
    print("Other Settings HISTORY_LENGTH:", history_length)
#    print()

    # Perform relay driving logic using these settings
    # ...
    print("*** ending  'use_local_settings_1.py  do_something_else() ***")
    print("=" * 62)
    update_check()
"""

# Example usage
# do_something()

# print("Other Settings WT_s:", wt_s)
# print(COLD_SETTINGS)
# print(WARM_SETTINGS)
# print(OTHER_SETTINGS)
# print()
# print(ALL_SETTINGS)

# print("Cold Settings - CON_p:", CON_p + 3)


# if __name__ == "__use_local_settings_1__":
"""
def update_check():
    
    print("=" * 60)    
    # Access the OTHER_SETTINGS
    print(" = OTHER_SETTINGS.get('WT_s') is :", WT_s)
    print(" = OTHER_SETTINGS.get('HISTORY_LENGTH') is :", history_length)
    print(" = OTHER_SETTINGS.get('last_modified') is :", last_modified)
    print(" = OTHER_SETTINGS.get('SENSOR_1_ROM') is :", SENSOR_1_ROM)
    print(" = OTHER_SETTINGS.get('SENSOR_2_ROM') is :", SENSOR_2_ROM)
    print(" = OTHER_SETTINGS.get('SENSOR_3_ROM') is :", SENSOR_3_ROM)
    
    print("=" * 60)
    # Access the COLD SETTINGS
    print("COLD_SETTINGS.get('CON_p') is :", CON_p_cold)
    print("COLD_SETTINGS.get('COF_d') is :", COF_d_cold)
    print(" = COLD_SETTINGS.get('HON_p') is :", HON_p_cold)
    print(" = COLD_SETTINGS.get('HOF_d') is :", HOF_d_cold)
    print(" = COLD_SETTINGS.get('CON_os') is :", CON_os_cold)
    print(" = COLD_SETTINGS.get('COF_os') is :", COF_os_cold)
    print(" = COLD_SETTINGS.get('HON_os') is :", HON_os_cold)
    print(" = COLD_SETTINGS.get('HOF_os') is :", HOF_os_cold)
    print(" = COLD_SETTINGS.get('WT_so') is :", WT_so_cold)
    
    print("=" * 60)
    #Access the WARM_SETTINGS
    print(" = WARM_SETTINGS.get('CON_p') is :", CON_p_warm)
    print(" = WARM_SETTINGS.get('COF_d') is :", COF_d_warm)
    print(" = WARM_SETTINGS.get('HON_p') is :", HON_p_warm)
    print(" = WARM_SETTINGS.get('HOF_d') is :", HOF_d_warm)
    print(" = WARM_SETTINGS.get('CON_os') is :", CON_os_warm)
    print(" = WARM_SETTINGS.get('COF_os') is :", COF_os_warm)
    print(" = WARM_SETTINGS.get('HON_os') is :", HON_os_warm)
    print(" = WARM_SETTINGS.get('HOF_os') is :", HOF_os_warm)
    print(" = WARM_SETTINGS.get('WT_so') is :", WT_so_warm)
    print("=" * 60)

#do_something()
#get_local_settings()


#=======================================================================#
#print(WT_s)
#te__relay_C_O_H__db__routs.send_2_server()
#get_tr_temps()

print("====== 'Fermenter_Settings.py' loaded ======")
#print()
get_local_settings()
update_check()
"""
