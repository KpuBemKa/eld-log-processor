from ..decoder import Decoder
from ..section.stat_data import StatDataDecoder

from modules.models.protocols.model_400C import Protocol400CModel


class Protocol400CDecoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = Protocol400CModel()

    def decode(self):
        self.__stat_data().__protocol_data()
        return self

    def get_result(self):
        return self.result

    def __stat_data(self):
        data = StatDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.stat_data = data.get_model()

        return self

    def __protocol_data(self):
        self.result.card_id = self.data[self.position :]

        return self
