from modules.response.response import Response


class PacketResponder:
    _parsed_packets: list[dict]

    def __init__(self, parsed_packets: list[dict]) -> None:
        self._parsed_packets = parsed_packets

    def make_responses(self):
        responses = []

        for packet in self._parsed_packets:
            response = Response(packet).make()
            if response:
                responses.append(response)

        return responses
