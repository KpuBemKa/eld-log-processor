class TrailerModel:
    crc = None
    protocol_tail = None

    def set(self, param, value):
        setattr(self, param, value)

        return self

    def get(self, param):
        return getattr(self, param)