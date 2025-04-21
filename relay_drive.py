# Relay Drive

print("I ========== START IMPORT 'relay_drive.py'                ========== I")

from machine import Pin

# Initialize GPIO32 and GPIO33 as outputs
relay1 = Pin(32, Pin.OUT)
relay2 = Pin(33, Pin.OUT)


def act_rel_1():
    relay1.value(0)  # Turn on relay connected to GPIO32


def d_act_rel_1():
    relay1.value(1)  # Turn off relay connected to GPIO32


def act_rel_2():
    relay2.value(0)  # Turn on relay connected to GPIO33


def d_act_rel_2():
    relay2.value(1)  # Turn off relay connected to GPIO33


def Cool_ON():
    relay1.value(0)  # Turn on relay connected to GPIO32


#    print("Relay-cool activated")


def Heat_ON():
    relay2.value(0)  # Turn on relay connected to GPIO33


#    print("Relay-heat activated")


def Cool_OFF():
    relay1.value(1)  # Turn off relay connected to GPIO32


#    print("Relay-cool deactivated")


def Heat_OFF():
    relay2.value(1)  # Turn off relay connected to GPIO33


#    print("Relay-heat deactivated")

Cool_OFF()
Heat_OFF()

print("I ==========   END IMPORT 'relay_drive.py'                ========== I")
