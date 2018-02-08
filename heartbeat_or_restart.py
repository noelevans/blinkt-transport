import os
import re
import requests
import subprocess
import sys


def available_wifi_names():
    response = subprocess.check_output('sudo iwlist wlan0 scan', shell=True)
    for line in response.split('\n'):
        match = re.match('.*ESSID:"(.*)"', line)
        if match:
            ssids.append(match.groups()[0])


def main():
    # Unknown error raised when the wifi adapter dies - restart RPi to "fix"
    url = 'http://www.google.com'
    try:
        requests.packages.urllib3.disable_warnings()
        _ = requests.get(url)
        print('Successful ping')
    except:
        sys.stderr.write('Failure to connect to Google. Restarting.\n')
        os.system('sudo shutdown -r now')


if __name__ == '__main__':
    main()
