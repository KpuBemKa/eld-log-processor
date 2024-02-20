""" Protocol trailer/footer/tail/end decoder """

import struct

from modules.models.packet.trailer import TrailerModel
from .decoder import Decoder


# https://docs.python.org/3/library/struct.html
TRAILER_UNPACK_STR = "<HH"


class TrailerDecoder(Decoder):
    """Protocol trailer/footer/tail/end decoder"""

    _data: bytes
    _model: TrailerModel = TrailerModel()

    def __init__(self, data: bytes):
        self._data = data

    def decode(self):
        (crc, tail) = struct.unpack_from(TRAILER_UNPACK_STR, self._data, len(self._data) - 4)

        self._model.crc = int.from_bytes(crc, byteorder="little")
        self._model.protocol_tail = tail

        return self

    def get_model(self) -> TrailerModel:
        """
        Returns trailer model as a dictionary
        """
        return self._model
