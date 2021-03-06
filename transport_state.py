import argparse
import blinkt
import colours
import requests
import time
import yaml


REFRESH_TIME = 10 * 60
ILLUMINATED_INTENSITY = 0.04


def typo_correct(input):
    subs = {
        'hamm': 'hammersmith-city',
        'over': 'london-overground',
        'rail': 'tfl-rail',
        'doc':  'dlr',
        'met':  'metropolitan',
        'pic':  'piccadilly',
        'tfl':  'tfl-rail',
        'wat':  'waterloo-city',
    }
    for k, v in subs.items():
        if input.startswith(k):
            return v
    return input


def user_choices():
    path = '/home/pi/repo/blinkt-transport/config.yml'
    cfg = yaml.load(open(path))

    raw_lines = cfg['lines'][:8]
    lines = []
    for el in raw_lines:
        line = el.strip().replace('\n', '').replace('\r', '').lower()
        lines.append(typo_correct(line))

    flashes = cfg['flash']
    return lines, flashes

def transport_status():
    status_aliases = {'Good Service': 'good',
                      'Minor Delays': 'ok'}   # All other statuses are 'bad'
    requests.packages.urllib3.disable_warnings()
    url = ('https://api.tfl.gov.uk/Line/Mode/' +
        'tube,dlr,overground,tflrail,tram/Status')
    resp = requests.get(url, timeout=5).json()

    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in resp}
    return {k: status_aliases.get(statuses[k], 'bad') for k in statuses.keys()}


def illuminate():
    lines, flashes = user_choices()
    all_statuses = transport_status()
    status = [all_statuses.get(el) for el in lines]
    line_colours = [colours.LINE_COLOURS.get(el, (0, 0, 0)) for el in lines]

    start = time.time()
    count = 0

    while time.time() < start + REFRESH_TIME:
        for n, (rgb, state) in enumerate(zip(line_colours, status)):
            if state:
                active = flashes[state]
                brightness = (count % active == 0) * ILLUMINATED_INTENSITY

                blinkt.set_pixel(n, *rgb, brightness=brightness)

        blinkt.show()
        count = count + 1
        time.sleep(1.0)


def main():
    # Adding an option to pause running if started from cron on power-up when
    # wifi adapter may not be ready causing a reboot and then indefinite loop
    parser = argparse.ArgumentParser()
    parser.add_argument('--init_wait', type=int, default=0)
    args = parser.parse_args()
    time.sleep(args.init_wait)

    while True:
        illuminate()


if __name__ == '__main__':
    main()
