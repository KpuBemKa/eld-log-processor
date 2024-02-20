class HeaderModel:
    protocol_head: bytes
    protocol_length: int
    protocol_version: str
    device_id: str
    device_bin_id: bytearray
    protocol_id: str

    def set(self, param, value):
        setattr(self, param, value)

        return self

    def get(self, param):
        return getattr(self, param)
