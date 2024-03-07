import socket
from socket import socket as Socket
import threading

from .conn_manager import ConnectionManager


class TCPServer:
    socket: Socket
    connection = ""
    host = "192.168.50.193"
    port = 49810

    def __init__(self):
        self.socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = socket.gethostname()
        self.socket.bind((self.host, self.port))
        self.socket.listen(100000)
        
        print(self.host, self.port)

    def run(self):
        # ConnectionManager(connection=None, addr=None).run()

        while True:
            connection, addr = self.socket.accept()

            print("Connected by", addr)

            conn_manager = ConnectionManager(connection=connection, addr=addr)
            thread = threading.Thread(target=conn_manager.run)
            thread.start()

        self.socket.close()
