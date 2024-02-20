from ..decoder import Decoder

from ..section.stat_data import StatDataDecoder
from ..section.gps_data import GPSDataDecoder


from modules.models.protocols.model_400D import Protocol400DModel


class Protocol400CDecoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = Protocol400DModel()

    def decode(self):
        self.__stat_data().__gps_data().__protocol_data()
        return self

    def get_result(self):
        return self.result

    def __stat_data(self):
        data = StatDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.stat_data = data.get_model()

        return self

    def __gps_data(self):
        data = GPSDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.gps_data = data.get_model()

        return self

    def __protocol_data(self):
        self.result.ic_data = self.data[self.position :]

        return self
