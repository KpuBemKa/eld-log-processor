from .decoder import Decoder
from modules.models.header import HeaderModel


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
    _decode = ["device_id"]

    def __init__(self, data: bytes):
        self.data = data
        self.model = HeaderModel()

    def decode(self) -> "HeaderDecoder":
        for item in self._items:
            self.model.set(item, self.get_data_part(item))

        return self

    def get_data_part(self, item: str) -> bytes:
        # first = last = False

        # if len(self._items[item]) == 1:
        #     return self.data[self._items[item][0] :]

        data = self.data[self._items[item][0] : self._items[item][1]]

        if item in self._numberize:
            return int.from_bytes(data, byteorder="little")
        
        if item in self._decode:
            return data.decode()

        if item not in self._exclude_hex:
            return data.hex()

        return data

    def get_model(self):
        """
        Returns header model as a dictionary
        """
        return self.model.__dict__
