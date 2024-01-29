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

    def __run_thread(self, connection, addr):
        # return

        while True:
            try:
                data = connection.recv(1024)

                if not data:
                    break

                # todo: merge messages without endings and separate by character \r\n

                print("Received some data:")

                result = Protocol(addr).decode(data).processing().encode()

                if result is not None:
                    print("Response: ", result)
                    connection.send(result)

            except socket.error:
                print("Error Occured: ", socket.error)
                break

            except Exception as e:
                print("Exception occured: ", e, e.args)
                break

        connection.close()
