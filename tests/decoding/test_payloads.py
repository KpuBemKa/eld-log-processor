import unittest

from modules.decoding.payload.decoder_1001 import Protocol1001Decoder


GPS_ITEM1 = (
    b"\x09\x02\x0A"  # date
    b"\x12\x07\x0C"  # time
    b"\xC0\x90\x12\x06"  # latitude
    b"\x00\x37\xA0\x0A"  # longitude
    b"\xBB\x08"  # speed
    b"\x14\x05"  # direction
    b"\x4f"  # flags
)
GPS_ITEM2 = (
    b"\x14\x02\x0A"  # date
    b"\x06\x13\x0D"  # time
    b"\xC0\x90\x12\x06"  # latitude
    b"\x00\x37\xA0\x0A"  # longitude
    b"\xBB\x08"  # speed
    b"\x14\x05"  # direction
    b"\x4f"  # flags
)
GPS_DATA = b"\x02" + GPS_ITEM1 + GPS_ITEM2

VSTATE = (
    (0b01010101).to_bytes()
    + (0b10101010).to_bytes()
    + (0b11001100).to_bytes()
    + (0b00110011).to_bytes()
)

STAT_DATA = (
    (1708616163).to_bytes(4, byteorder="little", signed=False)
    + (1708616163).to_bytes(4, byteorder="little", signed=False)
    + (100_000).to_bytes(4, byteorder="little", signed=False)
    + (500).to_bytes(4, byteorder="little", signed=False)
    + (24_000).to_bytes(4, byteorder="little", signed=False)
    + (100).to_bytes(2, byteorder="little", signed=False)
    + VSTATE
    + (0).to_bytes(8)
)

PAYLOAD_1001 = (
    STAT_DATA
    + GPS_DATA
    + "1.3.5".ljust(32).encode(encoding="ascii")
    + "2.0.1".ljust(32).encode(encoding="ascii")
    + (2).to_bytes(2, byteorder="little", signed=False)
    + (0).to_bytes(4, byteorder="little", signed=False)
)


class TestPayloadDecoding(unittest.TestCase):
    def test_p_1001(self):
        pass
