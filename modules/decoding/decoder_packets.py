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
        """Decodes self._raw_packets into worakble objects

        Returns:
            DecoderPackets: self
        """
        for raw_packet in self._raw_packets:
            parsed = self.__parse_packet(raw_packet)

            if parsed:
                self._parsed_packets.append(parsed)

        return self

    def get_result(self) -> list[PacketModel]:
        """Returns deocded packets from self.parse()

        Returns:
            list[PacketModel]: decoded packets
        """
        return self._parsed_packets

    def __parse_packet(self, raw_packet: bytes) -> PacketModel | None:
        """Decodes a packet

        Args:
            raw_packet (bytes): raw packet

        Returns:
            PacketModel | None: a decoded packet or None if some error happened
        """
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
        """Calculates CRC16 X.25 for raw_packet

        Args:
            crc (int): extracted crc from the packet
            raw_packet (bytes): raw packet

        Returns:
            bool: True if crc check passed, False if not
        """
        calculated = libscrc.x25(raw_packet)

        if calculated != crc:
            print(
                f"CRC16 X.25 failed. Received: {crc}; Calculated: {calculated}.\n"
                "Packet:\n{raw_packet}"
            )
            return False

        return True
