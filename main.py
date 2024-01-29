# persistence.py, line 32: where data should be sent instead of localhost?

"""

To do event types:
- Logout
- Login  
- Engine Power-up w/ CLP (Engine Power-up with conventional location precision)
- Engine Shut-down w/ CLP
- Engine Power-up w/ RLP  (Engine Power-up with reduced location precision)
- Engine Shut-Down w/ RLP
- On Duty  
- Driving
- Sleeper
- Off Duty                    
- YM
- PC
- PC/YM Cleared
- Certification 1 - 9       
- Intermediate w/ CLP     ( Intermediate log with conventional location precision)
- Intermediate w/ RLP   (Intermediate log with reduced location precision)
- Power data diagnostic (cleared)
- Power data diagnostic
- ELD malfunction
- ELD Malfunction cleared

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
