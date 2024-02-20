""" Header decoder """

import struct

from modules.models.packet.header import HeaderModel
from .decoder import Decoder


# https://docs.python.org/3/library/struct.html
PROTOCOL_UNPACK_STR = "<HHB20sH"


class DecoderHeader(Decoder):
    """Header decoder class"""

    _data: bytes
    _model: HeaderModel = HeaderModel()

    # _items = {
    #     "protocol_head": [0, 2],
    #     "protocol_length": [2, 4],
    #     "protocol_version": [4, 5],
    #     "device_id": [5, 25],
    #     "device_id_bin": [5, 25],
    #     "protocol_id": [25, 27],
    # }
    # # binary device id is needed for the header of the response to device
    # _exclude_hex = ["device_id_bin"]
    # # protocol length value is used to determine packet validity along with crc
    # _numberize = ["protocol_length"]
    # _decode = ["device_id"]

    def __init__(self, data: bytes):
        self._data = data

    def decode(self) -> "DecoderHeader":
        (header, length, version, device_id, protocol_id) = struct.unpack(
            PROTOCOL_UNPACK_STR, self.data
        )

        self._model.protocol_head = header
        self._model.protocol_length = int.from_bytes(length, byteorder="little")
        self._model.protocol_version = version.decode()
        self._model.device_id = device_id.decode()
        self._model.device_bin_id = device_id
        self._model.protocol_id = protocol_id.hex()

        return self

    # def get_data_part(self, item: str) -> bytes:
    #     # first = last = False

    #     # if len(self._items[item]) == 1:
    #     #     return self.data[self._items[item][0] :]

    #     data = self.data[self._items[item][0] : self._items[item][1]]

    #     if item in self._numberize:
    #         return int.from_bytes(data, byteorder="little")

    #     if item in self._decode:
    #         return data.decode()

    #     if item not in self._exclude_hex:
    #         return data.hex()

    #     return data

    def get_model(self) -> HeaderModel:
        """
        Returns header model as a dictionary
        """
        return self._model
