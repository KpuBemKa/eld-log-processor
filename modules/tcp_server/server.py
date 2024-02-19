import socket
import threading

from modules.protocol.protocol import Protocol
from modules.parser.conn_manager import ConnectionManager
# from modules.decoder.header_decoder import HeaderDecoder


class TCPServer:
    socket = ""
    connection = ""
    host = "192.168.50.198"
    port = 49810

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
