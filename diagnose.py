import blinkt
import os
import re
import requests
import subprocess
import sys
import time


def available_wifi_names():
    response = subprocess.check_output('sudo iwlist wlan0 scan', shell=True)

    ssids = []
    for line in response.split('\n'):
        match = re.match('.*ESSID:"(.*)"', line)
        if match and match.groups()[0]:
            ssids.extend(match.groups())
    return ssids


def desired_wifi():
    response = subprocess.check_output('sudo iwconfig', shell=True)
    if response:
        first_line = response.split('\n')[0]
        match = re.match('.*ESSID:"(.*)"', first_line)
        if match:
            return match.groups()[0]


def can_ping_website():
    urls = ['http://www.google.com', 'http://www.bbc.co.uk']
    for u in urls:
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(u)
            if response and response.ok:
                return True
        except:
            pass

    return False


def supplicant_wifi_name():
    ssids = []
    with open('/etc/wpa_supplicant/wpa_supplicant.conf') as conf:
        for line in conf:
            match = re.match('.*ssid=\"(.*)\"', line)
            if match:
                ssids.extend(match.groups())
    return ssids


def can_ping():
    blinkt.set_brightness(0.04)
    orange = (239, 123, 16)

    def set_pixels(ps):
        for p in ps:
            blinkt.set_pixel(p, *orange)
        blinkt.show()
        time.sleep(2)

    # Flash all LEDs
    blinkt.set_all(*orange)
    blinkt.show()
    time.sleep(2)
    blinkt.set_all(0, 0, 0)
    blinkt.show()
    time.sleep(2)

    choices = available_wifi_names()
    if not choices:
        return False

    set_pixels([0, 1])

    connection = desired_wifi()
    if not connection:
        return False

    set_pixels([2, 3])

    if connection not in choices:
        return False

    set_pixels([4, 5])

    if not can_ping_website():
        return False

    set_pixels([6, 7])

    blinkt.set_all(0, 0, 0)
    blinkt.show()

    return True


def main():
    return can_ping()


if __name__ == '__main__':
    main()
