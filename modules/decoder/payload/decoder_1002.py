from ..decoder import Decoder
# from modules.models.protocol_1002 import Protocol1002Model

# from modules.models.gps_model import GPS_Model
from ..section.stat_data import StatDataDecoder
from ..section.gps_data import GPSDataDecoder


class Protocol1002Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}

    def decode(self):
        self.stat_data().gps_data()
        return self

    def stat_data(self):
        data = StatDataDecoder(self.data).decode()
        self.position += data.get_position()
        self.result.update({"stat_data": data.get_model()})
        return self

    def gps_data(self):
        data = GPSDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({"gps_data": data.get_model()})
        return self

    def get_result(self):
        return self.result