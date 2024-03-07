import struct

from modules.decoding.decoder import Decoder
from modules.decoding.section.stat_data import StatDataDecoder
from modules.decoding.section.gps_data import GPSDataDecoder

from modules.models.protocols.model_1001 import Protocol1001Model


LOGIN_UNPACK_STR = "<" + "32s" + "32s" + "H"
LOGIN_UNPACK_LEN = 66


class Protocol1001Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}

    def decode(self):
        self.stat_data().gps_data().protocol_data()
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

    def protocol_data(self):
        data = Protocol1001Model()

        (soft_ver, hard_ver, new_param_count) = struct.unpack(
            LOGIN_UNPACK_STR, self.data[self.position : self.move(LOGIN_UNPACK_LEN)]
        )

        data.software_version = str(soft_ver)
        data.hardware_version = str(hard_ver)
        data.new_parameter_count = new_param_count

        unpack_str = "H" * new_param_count
        data.new_parameters.extend(
            struct.unpack(unpack_str, self.data[self.position : self.move(new_param_count * 2)])
        )

        self.result.update(data.__dict__)

        return self

    def get_result(self):
        return self.result
