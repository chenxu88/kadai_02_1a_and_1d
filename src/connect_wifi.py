import network
import time

from config import WIFI_CONFIG

ssid = WIFI_CONFIG["ssid"]
pwd = WIFI_CONFIG["password"]

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    time.sleep(1)

    if not wlan.isconnected():
        print("Connecting Wi-Fi...")
        wlan.connect(ssid, pwd)

        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > 120:
                raise RuntimeError("Wi-Fi connection timeout")
            time.sleep(1)

    print("Wi-Fi connected:", wlan.ifconfig())
    return wlan