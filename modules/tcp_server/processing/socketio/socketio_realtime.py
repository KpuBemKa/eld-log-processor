import json

class SoketioRealtime():

    data = None

    def __init__(self, socket):
        self.socket = socket
    def process(self, data):
        self.data = data
        if 'gps_data' in self.data['payload']:
            self.set_gps_data()

    def set_gps_data(self):
        self.socket.emit('gps_data', self.data['payload']['gps_data']['gps_data'])
# ('realtime.gps.' + self.data['payload']['VIN'], json.dumps(self.data['payload']['gps_data']['gps_data']))
