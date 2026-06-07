import network
import time

from config import WIFI_CONFIGS


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    time.sleep(1)

    for wifi in WIFI_CONFIGS:
        ssid = wifi["ssid"]
        pwd = wifi["password"]

        wlan.active(False)
        time.sleep(1)
        wlan.active(True)
        time.sleep(1)

        if wlan.isconnected():
            return wlan

        print("Trying Wi-Fi:", ssid)
        wlan.connect(ssid, pwd)

        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > 20:
                print("Wi-Fi failed:", ssid)
                break
            time.sleep(1)

        if wlan.isconnected():
            print("Wi-Fi connected:", ssid)
            print("Network config:", wlan.ifconfig())
            return wlan

    raise RuntimeError("All Wi-Fi connections failed")