""" Main decoding """

import libscrc

from modules.models.packet.packet import PacketModel

from .decoder_trailer import TrailerDecoder
from .decoder_header import DecoderHeader
from .decoder_payload import PayloadDecoder


class DecoderPackets:
    """Main decoding class"""

    _raw_packets: list[bytes] = []

    _parsed_packets: list[PacketModel] = []

    def __init__(self, raw_packets: list[bytes]) -> None:
        self._raw_packets = raw_packets

    def parse(self) -> "DecoderPackets":
        for raw_packet in self._raw_packets:
            parsed = self.__parse_packet(raw_packet)

            if parsed:
                self._parsed_packets.append(parsed)

        return self

    def get_result(self) -> list[PacketModel]:
        return self._parsed_packets

    def __parse_packet(self, raw_packet: bytes) -> None | PacketModel:
        parsed_packet = PacketModel()

        # parse the header
        parsed_packet.header = DecoderHeader(raw_packet).decode().get_model()
        # parse the trailer/tail/footer
        parsed_packet.trailer = TrailerDecoder(raw_packet).decode().get_model()

        if not self.__verify_crc(parsed_packet.trailer.crc, raw_packet):
            return None

        parsed_packet.payload = (
            # parse the paylaod
            PayloadDecoder(parsed_packet.header.protocol_id, raw_packet).decode().get_result()
        )

        return parsed_packet

    def __verify_crc(self, crc: int, raw_packet: bytes) -> bool:
        calculated = libscrc.x25(raw_packet)

        if calculated != crc:
            print(f"CRC16 X25 failed. Received: {crc}; Calculated: {calculated}")
            return False

        return True
