from decoder_trailer import TrailerDecoder
from decoder_header import DecoderHeader
from decoder_payload import PayloadDecoder


class DecoderPackets:
    _raw_packets: list[bytes] = []
    _parsed_packets: list[dict] = []

    def __init__(self, raw_packets: list[bytes]) -> None:
        self._raw_packets = raw_packets

    def parse(self) -> "DecoderPackets":
        for raw_packet in self._raw_packets:
            parsed = self.__parse_packet(raw_packet)

            if parsed:
                self._parsed_packets.append(parsed)

        return self

    def get_result(self) -> list[dict]:
        return self._parsed_packets

    def __parse_packet(self, raw_packet: bytes) -> dict | None:
        parsed_packet = {}

        # parse the header
        parsed_packet["header"] = DecoderHeader(raw_packet).decode().get_model()
        # parse the trailer/tail/footer
        parsed_packet["trailer"] = TrailerDecoder(raw_packet).decode().get_model()

        if not self.__verify_crc(raw_packet):
            return None

        parsed_packet["payload"] = (
            # parse the paylaod
            PayloadDecoder(parsed_packet["header"]["protocol_id"], raw_packet).decode().get_result()
        )

        return parsed_packet

    def __verify_crc(self, raw_packet: bytes) -> bool:
        # to do
        return True
