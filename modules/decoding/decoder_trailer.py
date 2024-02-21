""" Protocol trailer/footer/tail/end decoder """

import struct

from modules.models.packet.trailer import TrailerModel
from .decoder import Decoder


# https://docs.python.org/3/library/struct.html
TRAILER_UNPACK_STR = "<H2s"


class TrailerDecoder(Decoder):
    """Protocol trailer/footer/tail/end decoder"""

    _data: bytes
    _model: TrailerModel = TrailerModel()

    def __init__(self, data: bytes):
        self._data = data

    def decode(self):
        """Decodes protocol trailer

        Returns:
            TrailerDecoder: self
        """
        (crc, tail) = struct.unpack_from(TRAILER_UNPACK_STR, self._data, len(self._data) - 4)

        self._model.crc = crc
        self._model.protocol_tail = tail

        return self

    def get_model(self) -> TrailerModel:
        """
        Returns decoding result as trailer model
        """
        return self._model
