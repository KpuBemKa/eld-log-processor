import socket
import time


class Main1001Response:
    response = {}

    def __init__(self, connection):
        self.connection = connection

    def make(self):
        # self.response['ip_address'] = socket.inet_aton(self.connection[0])[::-1]
        # self.response['port'] = self.connection[1].to_bytes(2, 'little')
        self.response["ip_address"] = socket.inet_aton("255.255.255.255")[::-1]
        self.response["port"] = int(0000).to_bytes(2, "little")
        self.response["server_time"] = int(time.time()).to_bytes(4, "little")
        return (
            self.response["ip_address"]
            + self.response["port"]
            + self.response["server_time"]
        )
