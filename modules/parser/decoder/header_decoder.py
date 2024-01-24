from .decoder import Decoder
from modules.parser.models.header import HeaderModel


class HeaderDecoder(Decoder):
    items = {
        "protocol_head": [0, 2],
        "protocol_length": [2, 4],
        "protocol_version": [4, 5],
        "device_id": [5, 25],
        "protocol_id": [25, 27],
    }
    exclude_hex = ["device_id"]

    def __init__(self, data: bytes):
        self.data = data
        self.model = HeaderModel()

    def decode(self) -> "HeaderDecoder":
        for item in self.items:
            data = self.get_data_part(item)

            if item not in self.exclude_hex:
                data = data.hex()

            self.model.set(item, data)

        return self

    def get_data_part(self, item: str) -> bytes:
        # first = last = False

        if len(self.items[item]) == 1:
            return self.data[self.items[item][0] :]

        return self.data[self.items[item][0] : self.items[item][1]]

    def get_model(self):
        """
        Returns header model as a dictionary
        """
        return self.model.__dict__
