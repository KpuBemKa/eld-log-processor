from modules.models.packet.packet import PacketModel

from .response import Response


class ResponseMaker:
    _parsed_packets: list[PacketModel]

    _packets = []

    def __init__(self, parsed_packets: list[PacketModel]) -> None:
        self._parsed_packets = parsed_packets

    def make(self):
        self.__make_responses().__make_requests()

        return self._packets

    def __make_responses(self):
        for packet in self._parsed_packets:
            response = Response(packet).make()

            if response:
                self._packets.append(response)

        return self

    def __make_requests(self):
        # TODO: PacketRequester
        for packet in self._parsed_packets:
            if packet.header.protocol_id == "1001":
                self._packets.append(Response(packet).make_request("2001"))

        return self
