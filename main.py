# persistence.py, line 32: where data should be sent instead of localhost?

import multiprocessing
from modules.tcp_server.server import TCPServer


def worker():
    TCPServer().run()

if __name__ == "__main__":
    p = multiprocessing.Process(target=worker)
    p.start()
