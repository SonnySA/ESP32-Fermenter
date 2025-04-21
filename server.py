"""
server.py
Module for server communication routines.
"""

import time
import ujson
import settings
import urequests
import save_clear_db

# Retrieve server URL from settings and debug
SERVER_URL = settings.get("SERVER_URL")
print("[DEBUG] server.py: SERVER_URL =", SERVER_URL)
if not SERVER_URL:
    # fallback to hardcoded default if none provided
    SERVER_URL = "http://192.168.2.101/FMuBruwer/FMuBruwer-3.php"
    print("[WARN] server.py: Using default SERVER_URL =", SERVER_URL)


def send_2_server(data):
    """Send JSON data dict to server and display response."""
    if not SERVER_URL:
        print("[ERROR] SERVER_URL not set. Aborting send_2_server.")
        return
    # Debug: show target and payload
    print("[DEBUG] send_2_server: SERVER_URL =", SERVER_URL)
    print("[DEBUG] send_2_server: payload =", data)
    text = "Communicating with Server"
    box_width = len(text) + 2
    print("waiting ....", end="")
    time.sleep(0.02)
    print("\r┌ " + text + " ┐")

    Response_code = None
    Response_cont = "N/A - Request Failed"
    try:
        # send JSON manually to avoid json-keyword issues
        payload = ujson.dumps(data)
        headers = {"Content-Type": "application/json"}
        print("[DEBUG] send_2_server: POST with payload=", payload)
        response = urequests.post(SERVER_URL, data=payload, headers=headers)
        Response_code = response.status_code
        Response_cont = response.text
        response.close()
        print("@956  response_cont is", Response_cont)
    except Exception as e:
        print("Error sending data:", str(e))
        print("@960  response_cont is", Response_cont)

    line_length = 12 + len(Response_cont)
    print("waiting .....", end="")
    time.sleep(0.02)
    print(
        "\r│  Server Response  "
        + " " * (line_length - 32)
        + "└"
        + "─" * (line_length - 27)
        + "┐"
    )
    print("│   Status Code:", Response_code, " " * (line_length - 20), "│")
    print("│   Content:", Response_cont, "│")
    print("└" + "─" * (line_length + 1) + "┘")

    # trigger any scheduled save/clear action
    save_clear_db.check_and_trigger_save()


def send_2_server_orr(data):
    """Alternate server routine (legacy)."""
    text = "Communicating with Server"
    box_width = len(text) + 2
    print("waiting ....", end="")
    time.sleep(0.02)
    print("\r┌ " + text + " ┐")

    try:
        response = urequests.post(SERVER_URL, json=data)
        Response_code = response.status_code
        Response_cont = response.text
        response.close()
    except Exception as e:
        print("Error sending data:", str(e))

    line_length = 12 + len(Response_cont)
    print("waiting .....", end="")
    time.sleep(0.02)
    print("\r┌  Server Response  " + "─" * (line_length - 32) + "┐")
    print("│   Status Code:", Response_code, "│")
    print("│   Content:", Response_cont, "│")
    print("└" + "─" * (line_length + 1) + "┘")

    save_clear_db.check_and_trigger_save()
