import binascii
import socket
import re

from modules.processing.processing import Processing
from .packet_parser import PacketParser
from .response import Response


class Parser:
    _connection = None
    _addr = None

    _parsed_packets: list[dict] = [{}]
    _last_incomplete_packet: bytes = b""

    def __init__(self, connection, addr) -> None:
        self._connection = connection
        self._addr = addr

    def run(self) -> None:
        while True:
            try:
                data: bytes = self._connection.recv(1024)

                if not data:
                    break

                # parse raw binary data into parsed packets in form of dictionaries
                self.__data_to_packets(data)

                # process packets
                self.__process_packets()

                # respond back to the ELD
                self.__respond_back()

                # empty the list of packets
                self._parsed_packets = [{}]

            except socket.error as e:
                print("Socket error occured: ", e, e.args)
                break

            except Exception as e:
                print("Exception occured: ", e, e.args)
                break

        self._connection.close()

    def __data_to_packets(self, data: bytes) -> None:
        print("Data:\n", data)

        raw_packets = self.__extract_packets(data)

        for raw_packet in raw_packets:
            packet = PacketParser(raw_packet).parse().get_result()
            self._parsed_packets.append(packet)

            print("Hex:\n", binascii.hexlify(bytearray(raw_packet)))
            print("Parsed:\n", packet)

        print("\n\n")

    def __extract_packets(self, data: bytes) -> list[bytes]:
        # regex for splitting
        pattern = re.compile(b"(@@.*?\r\n)", re.DOTALL)

        # find all matches in the byte array
        sections = pattern.split(data)

        # filter out empty sections
        sections = [section for section in sections if section]

        # check if first section doesn't have a packet start
        if sections[0][:2] != b"\x40\x40":
            # if it doesn't have one, it's a piece of the last packet
            sections.append(self._last_incomplete_packet + sections[0])
            sections.pop(0)

        # check if last section doesn't have a packet end
        index = len(sections) - 1
        if sections[index][-2:] != b"\x0D\x0A":
            # if it doesn't have one, it's an incomplete packet
            self._last_incomplete_packet = sections[index]
            sections.pop(index)
        else:
            self._last_incomplete_packet = b""

        return sections

    def __process_packets(self):
        for packet in self._parsed_packets:
            Processing(packet).process()

    def __respond_back(self):
        for packet in self._parsed_packets:
            response = Response(self._connection, packet).make()

            if response is not None:
                self._connection.send(response)
