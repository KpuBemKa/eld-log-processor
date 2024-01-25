from .decoder.trailer_decoder import TrailerDecoder
from .decoder.header_decoder import HeaderDecoder
from .decoder.payload_decoder import PayloadDecoder


class PacketParser:
    _raw_packets: list[bytes]
    _parsed_packets: list[dict]

    def __init__(self, raw_packets: list[bytes]) -> None:
        self._raw_packets = raw_packets

    def parse(self) -> "PacketParser":
        for raw_packet in self._raw_packets:
            parsed = self.__parse_packet(raw_packet)

            if parsed:
                self._parsed_packets.append(parsed)

        return self

    def get_result(self) -> list[dict]:
        return self._parsed_packets

    def __parse_packet(self, raw_packet: bytes) -> dict | None:
        parsed_packet = {}

        parsed_packet["header"] = HeaderDecoder(raw_packet).decode().get_model()
        parsed_packet["trailer"] = TrailerDecoder(raw_packet).decode().get_model()

        if not self.__verify_crc(raw_packet):
            return self

        parsed_packet["payload"] = (
            PayloadDecoder(self.__parsed["header"]["protocol_id"], raw_packet).decode().get_result()
        )

        return parsed_packet

    def __verify_crc(self, raw_packet: bytes) -> bool:
        # to do
        return True
