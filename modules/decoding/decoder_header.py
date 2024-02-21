""" Header decoder """

import struct

from modules.models.packet.header import HeaderModel
from .decoder import Decoder


# https://docs.python.org/3/library/struct.html
PROTOCOL_UNPACK_STR = "<2sH1s20sH"


class DecoderHeader(Decoder):
    """Header decoder class"""

    _data: bytes
    _model: HeaderModel = HeaderModel()

    def __init__(self, data: bytes):
        self._data = data

    def decode(self) -> "DecoderHeader":
        (header, length, version, device_id, protocol_id) = struct.unpack(
            PROTOCOL_UNPACK_STR, self._data
        )

        self._model.protocol_head = header
        self._model.protocol_length = length
        self._model.protocol_version = version.hex()
        self._model.device_id = device_id.decode()
        self._model.device_bin_id = device_id
        self._model.protocol_id = hex(protocol_id)[2:]  # stip leading '0x'

        return self

    def get_model(self) -> HeaderModel:
        """
        Returns header model
        """
        return self._model
