from modules.parser.models.header import HeaderModel
import libscrc


class HeaderResponse:
    def __init__(self, data):
        self.data = data
        self.model = HeaderModel()

    def make(self, payload, protocol):
        self.model.protocol_head = bytes.fromhex("40") + bytes.fromhex("40")
        self.model.protocol_length = (
            2 + 2 + 1 + 20 + 2 + self.get_protocol_length(payload) + 2 + 2
        ).to_bytes(2, "little")
        self.model.protocol_version = bytes.fromhex(
            self.data["header"]["protocol_version"]
        )
        self.model.device_id = self.data["header"]["device_id"]
        self.model.protocol_id = bytes.fromhex(protocol)
        self.model.crc = self.get_crc(payload)
        self.model.crc = int(self.model.crc).to_bytes(2, "little")
        self.model.protocol_tail = bytes.fromhex(self.data["header"]["protocol_tail"])
        return (
            self.model.protocol_head
            + self.model.protocol_length
            + self.model.protocol_version
            + self.model.device_id
            + self.model.protocol_id
            + payload
            + self.model.crc
            + self.model.protocol_tail
        )

    def get_protocol_length(self, payload):
        if payload is None:
            return 0

        return len(payload)

    def get_crc(self, payload):
        if payload is None:
            return libscrc.x25(
                self.model.protocol_head
                + self.model.protocol_length
                + self.model.protocol_version
                + self.model.device_id
                + self.model.protocol_id
            )

        return libscrc.x25(
            self.model.protocol_head
            + self.model.protocol_length
            + self.model.protocol_version
            + self.model.device_id
            + self.model.protocol_id
            + payload
        )
