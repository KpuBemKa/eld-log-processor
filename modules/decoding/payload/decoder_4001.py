import struct

from modules.decoding.decoder import Decoder
from modules.decoding.section.stat_data import StatDataDecoder
from modules.decoding.section.gps_data import GPSDataDecoder

from modules.models.protocols.model_4001 import Protocol4001Model


class Protocol4001Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}

    def decode(self):
        self.protocol_data().stat_data().gps_data().rpm_data()
        return self

    def protocol_data(self):
        data = Protocol4001Model()
        data.flag = self.data[0]
        self.move(1)

        self.result.update(data.__dict__)

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

    def rpm_data(self):
        count = self.data[0]
        self.move(1)

        unpack_str = "H" * count
        raw_data = self.data[self.position : self.move(count * 2)]
        items: list[int] = []
        items.extend(struct.unpack(unpack_str, raw_data))

        self.result.update({"rpm_data": items})

        return self

    def get_result(self):
        return self.result
