import socket
import threading
import time

from .packet_parser import PacketParser
from .packet_responder import PacketResponder
from .packet_processor import PacketProcessor
from .packet_requester import PacketRequester
# from .response.response import Response

PACKET_START = b"\x40\x40"  # @@
PACKET_END = b"\x0D\x0A"  # \r\n


class ConnectionManager:
    _addr = None
    _connection = None

    _data = bytearray(b"")

    _raw_packets = []
    _raw_packets_lock = threading.Lock()

    def __init__(self, connection, addr) -> None:
        self._connection = connection
        self._addr = addr

    def run(self) -> None:
        receiver_thread = threading.Thread(target=self.__data_receiver, daemon=True)
        processor_thread = threading.Thread(target=self.__packet_processor, daemon=True)

        try:
            receiver_thread.start()
            processor_thread.start()

            receiver_thread.join()
            processor_thread.join()
        except socket.error as e:
            print("Socket error: ", e, e.args)
        except Exception as e:
            print("Exception occured: ", e, e.args)

        self._connection.close()
        print("Connection on port `", self._addr, "` has been terminated.")

    def __data_receiver(self):
        while True:
            try:
                received_data = self._connection.recv(1024)

                if not received_data:
                    break

                self._data.extend(received_data)

                packets = self.__extract_all_packets()
                if not packets:
                    continue

                with self._raw_packets_lock:
                    self._raw_packets.extend(packets)
            except socket.error as e:
                raise e
            except Exception as e:
                print("Exception during data receiving: ", e, e.args)

    def __packet_processor(self):
        while True:
            try:
                time.sleep(0.5)

                if not self._raw_packets:
                    continue

                with self._raw_packets_lock:
                    raw_packets = self._raw_packets
                    self._raw_packets = []

                parsed_packets = PacketParser(raw_packets).parse().get_result()
                print("Parsed:\n", parsed_packets)

                responses = []
                responses.extend(PacketResponder(parsed_packets).make_responses())
                responses.extend(PacketRequester(parsed_packets).make_requests())

                for response in responses:
                    self._connection.send(response)

                PacketProcessor(parsed_packets).process()

            except Exception as e:
                print("Error during packet processing: ", e, e.args)

    def __extract_all_packets(self) -> list[bytes]:
        packets = []

        index = 0
        end = len(self._data)

        while True:
            # find first occurence of packet start
            # -1 will be returned if none found
            index = self._data.find(PACKET_START, index, end)
            if index == -1:
                break

            # append a new packet if one was found
            raw_packet = self.__try_extract_packet(index)
            if raw_packet:
                packets.append(raw_packet)

            # increment the index, to not find the same packet
            index += len(PACKET_START)

        return packets

    def __try_extract_packet(self, index: int) -> bytes | None:
        # extract packet length which is next after packet start bytes
        packet_len = int.from_bytes(self._data[index + 2 : index + 4], byteorder="little")

        # if supposed packet length is bigger than _data length,
        # it is either an incomplete packet or a false positive
        # either way, it should not be extracted
        if packet_len > len(self._data):
            return None

        end_index = index + packet_len
        packet_end = self._data[index + end_index - 2 : index + end_index]

        # check if packet_length is correct, and points to the packet end sequence
        if packet_end != PACKET_END:
            return None

        # if it points to the right sequence, save the raw packet
        raw_packet = self._data[index:end_index]

        # delete it from the received buffer
        del self._data[index:end_index]

        # and return it
        return raw_packet
