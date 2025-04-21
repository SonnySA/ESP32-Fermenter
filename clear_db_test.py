import urequests


def trigger_save_and_clear():
    url = "http://192.168.2.40/FMuBruwer/export-clear-script.php"
    response = None
    try:
        print("Attempting to connect...")
        response = urequests.get(url, timeout=15)
        print("Response status:", response.status_code)
        print("Response text:", response.text)
        print("=" * 80)
        return True
    except Exception as e:
        print("Error triggering save and clear:", str(e))
        return False
    finally:
        if response:
            response.close()


def trigger_save_and_clear_2():
    import time

    url = "http://192.168.2.40/FMuBruwer/export-clear-script.php"
    response = None
    try:
        time.sleep(1)  # Add a small delay
        print("Attempting to connect...")
        response = urequests.get(url, timeout=15)
        print("Response status:", response.status_code)
        print("Response text:", response.text)
        print("=" * 80)
        return True
    except Exception as e:
        print("Error triggering save and clear:", str(e))
        return False
    finally:
        if response:
            response.close()


import socket


def test_connection():
    try:
        addr = socket.getaddrinfo("192.168.2.40", 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        print("Connection successful")
        s.close()
    except Exception as e:
        print("Connection test failed:", str(e))


# trigger_save_and_clear_2()
