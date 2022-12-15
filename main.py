import gc
import time
import network
import socket
import ujson as json

from secrets import WIFI_SSID, WIFI_PASS
from sensor import CO2Sensor, COSensor
from machine import Pin

ADDR = ("192.168.1.69", 5555)

def wifi_connect():
    rp2.country('AU')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    # WiFi Connection code from https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
    max_wait = 10
    for _ in range(max_wait):
        status = wlan.status()
        if status < 0 or status >= 3:
            break
        time.sleep(1)

    if wlan.status() != 3:
        print('wifi connection failed')
        wlan.active(False)

    ip = wlan.ifconfig()[0]
    print('WiFi connected; ip = ' + ip)
    return wlan


wifi_connect()
s = CO2Sensor()
s2 = COSensor()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
while True:
    payload = json.dumps({'temperature': s.temp, 'humidity': s.hum, 'co2_ppm': s.co2, 'co_ppm': s2.co})
    sock.sendto(payload, ADDR)
    gc.collect()
    time.sleep(1.0)
"""

# On a discrete RTC
s.measure_wait()
s2.measure()
payload = json.dumps({'temperature': s.temp, 'humidity': s.hum, 'co2_ppm': s.co2, 'co_ppm': s2.co})
print(payload)
sock.sendto(payload, ADDR)
Pin(22, Pin.OUT).on() # DONE for Makerverse Nano Power Timer HAT

