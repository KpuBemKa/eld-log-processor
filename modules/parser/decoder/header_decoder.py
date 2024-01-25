from .decoder import Decoder
from modules.parser.models.header import HeaderModel


class HeaderDecoder(Decoder):
    _items = {
        "protocol_head": [0, 2],
        "protocol_length": [2, 4],
        "protocol_version": [4, 5],
        "device_id": [5, 25],
        "device_id_bin": [5, 25],
        "protocol_id": [25, 27],
    }
    # binary device id is needed for the header of the response to device  
    _exclude_hex = ["device_id_bin"]
    # protocol length value is used to determine packet validity along with crc
    _numberize = ["protocol_length"]

    def __init__(self, data: bytes):
        self.data = data
        self.model = HeaderModel()

    def decode(self) -> "HeaderDecoder":
        for item in self._items:
            data = self.get_data_part(item)

            if item not in self._exclude_hex:
                data = data.hex()

            if item in self._numberize:
                data = int.from_bytes(data, byteorder="little")

            self.model.set(item, data)

        return self

    def get_data_part(self, item: str) -> bytes:
        # first = last = False

        # if len(self._items[item]) == 1:
        #     return self.data[self._items[item][0] :]

        return self.data[self._items[item][0] : self._items[item][1]]

    def get_model(self):
        """
        Returns header model as a dictionary
        """
        return self.model.__dict__
