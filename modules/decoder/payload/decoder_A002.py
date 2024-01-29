from ..decoder import Decoder
from modules.models.model_A002 import ProtocolA002Model


class ProtocolA002Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}

    def decode(self):
        self.protocol_data()
        return self

    def protocol_data(self):
        data = ProtocolA002Model()
        data.cmd_seq = self.data[self.position : self.move(2)]
        data.resp_count = self.data[self.position : self.move(1)]
        data.resp_index = self.data[self.position : self.move(1)]
        data.fail_count = self.data[self.position : self.move(1)]

        #

        self.result.update(data.__dict__)

        return self

    def get_result(self):
        return self.result
