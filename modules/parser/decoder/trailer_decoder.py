from .decoder import Decoder
from modules.parser.models.trailer import TrailerModel


class TrailerDecoder(Decoder):
    items = {
        "crc": [-4, -2],
        "protocol_tail": [-2],
    }

    def __init__(self, data: bytes):
        self.data = data
        self.model = TrailerModel()

    def decode(self):
        for item in self.items:
            data = self.get_data_part(item)

            data = data.hex()

            self.model.set(item, data)

        return self

    def get_data_part(self, item):
        if len(self.items[item]) == 1:
            return self.data[self.items[item][0] :]

        return self.data[self.items[item][0] : self.items[item][1]]

    def get_model(self):
        """
        Returns trailer model as a dictionary
        """
        return self.model.__dict__
