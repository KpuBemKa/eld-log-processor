import libscrc

from modules.models.packet.header import HeaderModel
from modules.models.packet.packet import PacketModel
from modules.models.packet.trailer import TrailerModel


class HeaderResponse:
    def __init__(self, data: PacketModel):
        self._packet = data

        self.header_model = HeaderModel()
        self.trailer_model = TrailerModel()

    def make(self, payload, protocol):
        self.header_model.protocol_head = b"\x40\x40"
        self.header_model.protocol_length = (
            2 + 2 + 1 + 20 + 2 + self.get_protocol_length(payload) + 2 + 2
        )
        self.header_model.protocol_version = self._packet.header.protocol_version
        self.header_model.device_bin_id = self._packet.header.device_bin_id
        self.header_model.protocol_id = protocol
        self.trailer_model.crc = int(self.get_crc(payload))
        self.trailer_model.protocol_tail = self._packet.trailer.protocol_tail

        return (
            self.header_model.protocol_head
            + self.header_model.protocol_length.to_bytes(2, "little")
            + bytes.fromhex(self.header_model.protocol_version)
            + self.header_model.device_bin_id
            + bytes.fromhex(self.header_model.protocol_id)
            + payload
            + self.trailer_model.crc.to_bytes(2, "little")
            + self.trailer_model.protocol_tail
        )

    def get_protocol_length(self, payload):
        if payload is None:
            return 0

        return len(payload)

    def get_crc(self, payload):
        if payload is None:
            return libscrc.x25(
                self.header_model.protocol_head
                + self.header_model.protocol_length.to_bytes(2, "little")
                + bytes.fromhex(self.header_model.protocol_version)
                + self.header_model.device_bin_id
                + bytes.fromhex(self.header_model.protocol_id)
            )

        return libscrc.x25(
            self.header_model.protocol_head
            + self.header_model.protocol_length.to_bytes(2, "little")
            + bytes.fromhex(self.header_model.protocol_version)
            + self.header_model.device_bin_id
            + bytes.fromhex(self.header_model.protocol_id)
            + payload
        )
