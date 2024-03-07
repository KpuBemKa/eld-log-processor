import struct
from modules.decoding.decoder import Decoder
from modules.decoding.section.stat_data import StatDataDecoder
from modules.models.protocols.model_4008 import Protocol4008Model


UNPACK_STR = "<HH"


class Protocol4008Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}
        self.model = Protocol4008Model()

    def decode(self):
        self.stat_data().protocol_data()
        return self

    def stat_data(self):
        data = StatDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({"stat_data": data.get_model()})

        return self

    def protocol_data(self):
        raw_data = self.data[self.position : self.move(4)]
        (local_area_code, cell_id) = struct.unpack(UNPACK_STR, raw_data)

        self.model.local_area_code = local_area_code
        self.model.cell_id = cell_id

        self.result.update(self.model.__dict__)

        return self

    def get_result(self):
        return self.result
