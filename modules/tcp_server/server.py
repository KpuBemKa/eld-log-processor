import socket
import _thread
from modules.parser.protocol.protocol import Protocol
from modules.parser.parser import Parser
# from modules.parser.decoder.header_decoder import HeaderDecoder


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
        while True:
            connection, addr = self.socket.accept()
            print("Connected by", addr)
            _thread.start_new_thread(self.run_thread, (connection, addr))

        self.socket.close()

    def run_thread(self, connection, addr):
        Parser(connection=connection, addr=addr).run()    
        
        # return    
        
        # while True:
        #     try:
        #         data = connection.recv(1024)

        #         if not data:
        #             break

        #         # todo: merge messages without endings and separate by character \r\n
                
        #         print("Received some data:")

        #         result = Protocol(addr).decode(data).processing().encode()

        #         if result is not None:
        #             print("Response: ", result)
        #             connection.send(result)

        #     except socket.error:
        #         print("Error Occured: ", socket.error)
        #         break
            
        #     except Exception as e:
        #         print("Exception occured: ", e, e.args)
        #         break

        # connection.close()
