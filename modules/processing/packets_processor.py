from modules.processing.processing import Processing


class PacketProcessor:
    _parsed_packets: list[dict]

    def __init__(self, parsed_packets: list[dict]) -> None:
        self._parsed_packets = parsed_packets

    def process(self) -> "PacketProcessor":
        for packet in self._parsed_packets:
            Processing().process(packet)
