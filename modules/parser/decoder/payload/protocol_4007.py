from ..decoder import Decoder
# from modules.parser.models.protocol_4001 import Protocol4001Model
from modules.parser.models.protocol_4007 import Protocol4007Model

from ..section.stat_data import StatDataDecoder
from ..section.gps_data import GPSDataDecoder
from ..section.alarm_data import AlarmDataDecoder


class Protocol4007Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}
        self.model = Protocol4007Model()

    def decode(self):
        self.protocol_data_one().stat_data().gps_data().protocol_data_two()
        return self

    def stat_data(self):
        data = StatDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({"stat_data": data.get_model()})

        return self

    def gps_data(self):
        data = GPSDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({"gps_data": data.get_model()})

        return self

    def protocol_data_one(self):
        self.model.alarm_seq = self.data[self.position : self.move(4)]

        return self

    def protocol_data_two(self):
        decoded = AlarmDataDecoder(self.data, start=self.position).decode().get_model()
        self.model.alarm_count = decoded.alarm_count
        self.model.alarm_array = decoded.alarm_data

        self.result.update(self.model.__dict__)

        return self

    def get_result(self):
        return self.result
