class HeaderModel:
    protocol_head = None
    protocol_length = None
    protocol_version = None
    device_id = None
    protocol_id = None
    crc = None
    protocol_tail = None

    def set(self, param, value):
        setattr(self, param, value)

        return self

    def get(self, param):
        return getattr(self, param)
