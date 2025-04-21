import network
import WiFi_Connect

print("WiFi_List.py @4 - starting init_wlan()")
WiFi_Connect.init_wlan()
print("WiFi_List.py @6- starting  scan_network(wlan)")
WiFi_Connect.scan_networks(network.WLAN(network.STA_IF))
print("WiFi_List.py @8 - starting  connect_to_best_wifi()")
print("")
print(f"Connected to WiFi network: {WiFi_Connect.get_current_ssid()}")
print("WiFi_List.py Complete @11")
