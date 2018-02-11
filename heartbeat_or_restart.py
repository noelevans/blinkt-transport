import os
import re
import requests
import subprocess
import sys


def available_wifi_names():
    response = subprocess.check_output('sudo iwlist wlan0 scan', shell=True)

    ssids = []
    for line in response.split('\n'):
        match = re.match('.*ESSID:"(.*)"', line)
        if match and match.groups()[0]:
            ssids.extend(match.groups())
    return ssids


def desired_wifi():
    response = subprocess.check_output('iwconfig', shell=True)
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


def main():
    # Flash all LEDs

    choices = available_wifi_names()

    connection = desired_wifi()

    connection in choices

    can_ping_website()

    """
    sys.stderr.write('Failure to connect to Google. Restarting.\n')
    os.system('sudo shutdown -r now')
    """

if __name__ == '__main__':
    main()
