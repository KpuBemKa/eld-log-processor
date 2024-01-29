from modules.models.header import HeaderModel
from modules.models.trailer import TrailerModel
import libscrc


class HeaderResponse:
    def __init__(self, data):
        self.data = data
        self.header_model = HeaderModel()
        self.trailer_model = TrailerModel()

    def make(self, payload, protocol):
        self.header_model.protocol_head = bytes.fromhex("40") + bytes.fromhex("40")
        self.header_model.protocol_length = (
            2 + 2 + 1 + 20 + 2 + self.get_protocol_length(payload) + 2 + 2
        ).to_bytes(2, "little")
        self.header_model.protocol_version = bytes.fromhex(self.data["header"]["protocol_version"])
        self.header_model.device_id = self.data["header"]["device_id_bin"]
        self.header_model.protocol_id = bytes.fromhex(protocol)
        self.trailer_model.crc = self.get_crc(payload)
        self.trailer_model.crc = int(self.trailer_model.crc).to_bytes(2, "little")
        self.trailer_model.protocol_tail = bytes.fromhex(self.data["trailer"]["protocol_tail"])
        return (
            self.header_model.protocol_head
            + self.header_model.protocol_length
            + self.header_model.protocol_version
            + self.header_model.device_id
            + self.header_model.protocol_id
            + payload
            + self.trailer_model.crc
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
                + self.header_model.protocol_length
                + self.header_model.protocol_version
                + self.header_model.device_id
                + self.header_model.protocol_id
            )

        return libscrc.x25(
            self.header_model.protocol_head
            + self.header_model.protocol_length
            + self.header_model.protocol_version
            + self.header_model.device_id
            + self.header_model.protocol_id
            + payload
        )
