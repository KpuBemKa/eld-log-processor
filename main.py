# persistence.py, line 32: where data should be sent instead of localhost?

"""

To do event types:
- Driver assignment 
- Engine Power-up & Shut-down (always marked as with max location precision)
- Driver status: [
    Driving,
    On Duty,
    Off Duty,
    Sleeping,
    YM (weather factor),
    PC (personal use),
    PC/YM Cleared
]
- Intermediate log once per hour of Driving (always marked as with max location precision)
- Power data diagnostic & Power data diagnostic cleared
- ELD malfunction & ELD Malfunction cleared

Done event types:


"""

import multiprocessing
from modules.tcp_server.server import TCPServer


def worker():
    TCPServer().run()


def main():
    p = multiprocessing.Process(target=worker, daemon=True)
    p.start()
    p.join()

    # while True:
    #     pass


if __name__ == "__main__":
    main()
