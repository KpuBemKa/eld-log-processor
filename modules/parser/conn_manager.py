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
    _connection: socket = None

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

                # append recevied data
                self._data.extend(received_data)

                # extracts packets from appeneded data
                packets = self.__extract_all_packets()

                if not packets:
                    continue

                # appened extracted packets, if any extracted
                with self._raw_packets_lock:
                    self._raw_packets.extend(packets)

                # extractor thread will parse and process these raw packets
            except socket.error as e:
                raise e
            except Exception as e:
                print("Exception during data receiving: ", e, e.args)

        self._connection.close()

    def __packet_processor(self):
        while True:
            try:
                time.sleep(0.5)

                # if no packets were received, go back to sleep
                if not self._raw_packets:
                    continue

                # copy extracted packets to local variable to release locked resources faster
                with self._raw_packets_lock:
                    # copy packets and clear the source
                    raw_packets = self._raw_packets
                    self._raw_packets = []

                # parse raw packets to dictionaries
                parsed_packets = PacketParser(raw_packets).parse().get_result()
                print("Parsed:\n", parsed_packets)

                # construct responses and requests to be sent back before processing the packets
                responses = []
                responses.extend(PacketResponder(parsed_packets).make_responses())
                responses.extend(PacketRequester(parsed_packets).make_requests())

                for response in responses:
                    self._connection.send(response)

                # process parsed packets
                PacketProcessor(parsed_packets).process()

            except Exception as e:
                print("Error during packet processing: ", e, e.args)

    def __extract_all_packets(self) -> list[bytes]:
        packets = []

        index = 0
        end = len(self._data)

        while True:
            # find first occurence of a packet start
            # -1 is returned if none found
            index = self._data.find(PACKET_START, index, end)
            if index == -1:
                break

            raw_packet = self.__try_extract_packet(index)

            if raw_packet:
                # if a packet was found, its sequence was deleted from the bytearray,
                # so just append it
                packets.append(raw_packet)
            else:
                # if not found, sequence was not deleted,
                # and index should be incremented by a bit to not find the same packet later
                index += len(PACKET_START)

        # return the array of extracted packets
        return packets

    def __try_extract_packet(self, index: int) -> bytes | None:
        # extract the supposed packet length which is next after packet-start bytes
        packet_len = int.from_bytes(self._data[index + 2 : index + 4], byteorder="little")

        # if supposed packet length is bigger than _data length,
        # it is either an incomplete packet or a false positive
        # either way, it should not be extracted
        if packet_len > len(self._data):
            return None

        end_index = index + packet_len
        packet_end = self._data[index + end_index - 2 : index + end_index]

        # check if packet_length is correct, and if it points to the packet end sequence
        if packet_end != PACKET_END:
            # if it doesn't point to a packet end sequence, this is not a packet,
            # and should not be extracted
            return None

        # save the raw packet
        raw_packet = self._data[index:end_index]

        # delete it from the received buffer
        del self._data[index:end_index]

        # and return it
        return raw_packet
