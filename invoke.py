import blinkt
import os

import diagnose
import transport_state


def main():
    if diagnose.can_ping():
        while True:
             transport_state.illuminate()
    else:
        blinkt.set_all(220, 36, 31, brightness=0.04)
        blinkt.show()
        os.system('sudo shutdown -h now')


if __name__ == '__main__':
    main()
