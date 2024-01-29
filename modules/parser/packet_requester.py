from modules.response.response import Response


class PacketRequester:
    _parsed_packets: list[dict]

    def __init__(self, parsed_packets: list[dict]) -> None:
        self._parsed_packets = parsed_packets

    def make_requests(self):
        requests = []

        for packet in self._parsed_packets:
            if packet["header"]["protocol_id"] == "1001":
                requests.append(Response(packet).make_request("2001"))

        return requests
