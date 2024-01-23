from ..decoder import Decoder
from modules.tcp_server.models.protocol_4001 import Protocol4001Model

from ..section.stat_data import StatDataDecoder
from ..section.gps_data import GPSDataDecoder


class Protocol4001Decoder(Decoder):

    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}


    def decode(self):
        self.protocol_data().stat_data().gps_data()
        return self

    def stat_data(self):
        data = StatDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({'stat_data': data.get_model()})

        return self

    def gps_data(self):
        data = GPSDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({'gps_data': data.get_model()})

        return self

    def protocol_data(self):
        data = Protocol4001Model()
        data.flag = self.data[self.position: self.move(1)]

        self.result.update(data.__dict__)

        return self

    def get_result(self):
        return self.result
