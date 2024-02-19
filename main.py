# persistence.py, line 32: where data should be sent instead of localhost?

"""

TODO event types:
+ Driver assignment -> uknown assignment protocol 

+ Driver status: [
    Driving,
    On Duty,
    Off Duty,
    Sleeping,
    YM (weather factor),
    PC (personal use),
    PC/YM Cleared
] -> unknown duty status protocol

- Power data diagnostic set & Power data diagnostic cleared

- ELD malfunction & ELD Malfunction cleared


Done event types:
- Engine Power-up & Shut-down (always marked as with max location precision)
- Intermediate log once per hour of DRIVING status active (always marked as with max location precision)


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
