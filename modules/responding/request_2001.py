import random


class TLV_Model:
    tag: int
    length: int
    switch: int
    threshold: int

    def __init__(self, tag, length, switch, threshold):
        self.tag = tag
        self.length = length
        self.switch = switch
        self.threshold = threshold

    def to_bytes(self):
        result = bytearray()
        result += self.tag.to_bytes(2, byteorder="little")
        result += self.length.to_bytes(2, byteorder="little")
        result += self.switch.to_bytes(1, byteorder="little")
        result += self.threshold.to_bytes(2, byteorder="little")

        return result


SETTINGS = bytearray(TLV_Model(tag=0x1001, length=3, switch=0b11, threshold=8).to_bytes())


class Request2001:
    # payload = {}

    def make(self):
        payload = bytearray()
        payload += random.randint(0, 65535).to_bytes(4, "little")
        payload += len(SETTINGS).to_bytes(1, byteorder="little")
        payload += SETTINGS

        return payload
