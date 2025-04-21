import urequests
import time
import random
from machine import Timer

# Configuration
PHP_ENDPOINT = "http://192.168.2.101/FMuBruwer/update_temps_2.php"
INTERVAL = 15  # Seconds between readings


def generate_dummy_temps():
    # Generate dummy temperatures with 3 decimal places
    w_t = 20.0 + random.random() * 2  # Range: 20.0 to 22.0
    c_t = 21.0 + random.random() * 2  # Range: 21.0 to 23.0
    o_t = 22.0 + random.random() * 2  # Range: 22.0 to 24.0

    return round(w_t, 3), round(c_t, 3), round(o_t, 3)


def send_temperatures():
    print("send start -")
    try:
        w_t, c_t, o_t = generate_dummy_temps()

        # Prepare data for POST request
        data = {"w_t": str(w_t), "c_t": str(c_t), "o_t": str(o_t)}

        # Send POST request
        response = urequests.post(PHP_ENDPOINT, json=data)

        print(f"Sent temperatures - W: {w_t}°C, C: {c_t}°C, O: {o_t}°C")
        print(f"Response: {response.text}")

        response.close()
        print("- send end")

    except Exception as e:
        print(f"Error sending data: {e}")


def main():
    while True:
        send_temperatures()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    # Connect to WiFi first (code not shown - use your existing WiFi connection code)
    main()
