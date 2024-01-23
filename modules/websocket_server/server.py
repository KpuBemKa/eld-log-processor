from aiohttp import web
import socketio

class WebsocketServer:

    socket = None
    server = None
    connection = ''
    host = "192.168.100.2"
    port = 10840

    def __init__(self):
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = socket.gethostname()
        # self.socket.bind((self.host, self.port))
        # self.socket.listen(100000)
        # print(self.host, self.port)
        self.socket = socketio.AsyncServer()
        self.server = web.Application()
        self.socket.attach(self.server)

    def run(self):
        self.socketio = socketio.Server()

        while True:
            connection, addr = self.socket.accept()
            print('Connected by', addr)
            _thread.start_new_thread(self.run_thread, (connection, addr))

        self.socket.close()

    def run_thread(self, connection, addr):
        while True:
            try:
                data = connection.recv(1024)

                if not data:
                    break

                result = Protocol(addr).decode(data).processing(self.socketio).encode()

                if result is not None:
                    connection.send(result)

            except socket.error:
                print("Error Occured.")
                break

        connection.close()
