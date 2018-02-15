import blinkt
import logging
import os
import time

import diagnose
import transport_state


def main():
    # While RPi starts, some services will come up earlier than others. Allow
    # execution to continue when URLs can be loaded or give up after 2 minutes.
    start_time = time.time()
    while (not diagnose.can_ping_website()) and time.time() < start_time + 120:
        time.sleep(5)

    if diagnose.can_ping():
        while True:
            try:
                transport_state.illuminate()
            except:
                # No restoration attempted - heartbeat script will manage it
                logging.exception('Problem updating blinkt')
    else:
        blinkt.set_all(220, 36, 31, brightness=0.04)
        blinkt.show()
        os.system('sudo shutdown -h now')


if __name__ == '__main__':
    main()
