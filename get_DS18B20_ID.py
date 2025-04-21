import machine
import onewire
import ds18x20
import time
import binascii  # Import binascii module

# Current ds18b20 sensors
# Sensor ID: 2876cea007000067  @250222 ROM3 ###
# Sensor ID: 289cfab20a000035  ###
# Sensor ID: 28a647b40a0000bd
# Sensor ID: 28aa3aa453140105  @250222 ROM1 ###
# Sensor ID: 28aa9f9b53140136  ###
# Sensor ID: 28aa88995314011c  @250222 ROM2 ###
# Sensor ID: 28ff67c602170317  ###

# Define the GPIO pin where the DS18B20 sensors are connected
ds_pin = machine.Pin(4)

# Initialize the 1-Wire bus
ow = onewire.OneWire(ds_pin)

# Initialize the DS18X20 object
ds = ds18x20.DS18X20(ow)

# Scan for devices on the bus
roms = ds.scan()
print("Found DS18B20 devices:")
for rom in roms:
    print(binascii.hexlify(rom).decode())  # Convert bytearray to hex string and print


# Function to read and print temperatures from all sensors
def read_temperatures():
    # Start temperature conversion
    ds.convert_temp()
    time.sleep_ms(750)  # Wait for the conversion to complete (usually 750ms)

    for rom in roms:
        # Read temperature from each sensor
        temperature = ds.read_temp(rom)
        rom_str = binascii.hexlify(rom).decode()  # Convert ROM ID to hex string
        print(f"Sensor ID: {rom_str}, Temperature: {temperature:.2f}°C")


# Loop to read and print temperatures every 10 seconds
loop = 1
while True:
    print("Read #", loop)
    read_temperatures()
    loop = loop + 1
    print()
    time.sleep(10)
