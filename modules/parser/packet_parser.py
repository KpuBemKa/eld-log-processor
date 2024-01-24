from .decoder.trailer_decoder import TrailerDecoder
from .decoder.header_decoder import HeaderDecoder
from .decoder.payload_decoder import PayloadDecoder


class PacketParser:
    __parsed = {}

    def __init__(self, raw_packet) -> None:
        self._raw_packet = raw_packet

    def parse(self) -> "PacketParser":
        self.__parsed["header"] = HeaderDecoder(self._raw_packet).decode().get_model()
        self.__parsed["trailer"] = TrailerDecoder(self._raw_packet).decode().get_model()

        if not self.__verify_ends():
            self.__parsed = None
            return self

        if not self.__verify_crc():
            self.__parsed = None
            return self

        self.__parsed["payload"] = (
            PayloadDecoder(self.__parsed["header"]["protocol_id"], self._raw_packet)
            .decode()
            .get_result()
        )

        return self

    def get_result(self):
        return self.__parsed

    def __verify_ends(self) -> bool:
        if self.__parsed["header"]["protocol_head"] != "4040":
            return False

        if self.__parsed["trailer"]["protocol_tail"] != "0d0a":
            return False

        return True

    def __verify_crc(self) -> bool:
        # to do
        return True
