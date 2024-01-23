import socket
import _thread
from modules.tcp_server.protocol.protocol import Protocol
from modules.tcp_server.decoder.header_decoder import HeaderDecoder

class TCPServer:
    socket = ''
    connection = ''
    host = "192.168.50.198"
    port = 49810


    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.socket.bind((self.host, self.port))
        self.socket.listen(100000)
        print(self.host, self.port)


    def run(self):
        while True:
            connection, addr = self.socket.accept()
            print('Connected by', addr)
            _thread.start_new_thread(self.run_thread, (connection, addr))

        self.socket.close()


    def run_thread(self, connection, addr):
        # data = b''
        while True:
            try:
                data = connection.recv(1024)

                if not data:
                    break

                #todo: merge messages without endings and separate by character \r\n

                result = Protocol(addr).decode(data).processing().encode()

                if result is not None:
                    connection.send(result)

            except socket.error:
                print("Error Occured.")
                break

        connection.close()
