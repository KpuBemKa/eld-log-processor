import socket
import threading
import time

from .packet_parser import PacketParser
from .packet_processor import PacketProcessor
# from .response.response import Response

# tried to do it with the regex but it's not reliable enough; payload can contain '\r\n', for example
PACKET_START = b"\x40\x40"  # @@
PACKET_END = b"\x0D\x0A"  # \r\n


class ConnectionManager:
    _connection = None
    _addr = None

    _data = bytearray(b"")
    _data_lock = threading.Lock()

    _raw_packets = []
    _raw_packets_lock = threading.Lock()

    def __init__(self, connection, addr) -> None:
        self._connection = connection
        self._addr = addr

    def run(self) -> None:
        receiver_thread = threading.Thread(target=self.__data_receiver, daemon=True)
        extractor_thread = threading.Thread(target=self.__packet_extractor, daemon=True)
        processor_thread = threading.Thread(target=self.__packet_processor, daemon=True)

        try:
            receiver_thread.start()
            extractor_thread.start()
            processor_thread.start()

            receiver_thread.join()
            extractor_thread.join()
            processor_thread.join()
        except Exception as e:
            print("Exception occured: ", e, e.args)

        self._connection.close()

    def __data_receiver(self):
        # data_sim = [
        #     b"@@Data for @section 1\r\n@@Data for sect",
        #     b"ion 2\r\n@@Data for section 3\r\n@@Data f",
        #     b"or section 4\r\n",
        # ]
        # data_sim = [
        #     bytearray.fromhex("4040330002000102030405060708090a0b0c0d0e0f101112"),
        #     bytearray.fromhex("130102000102030405060708090a0b0c0d0e0f1011121303040d0a"),
        #     bytearray.fromhex(
        #         "4040350002000102030405060708090a0b0c0d0e0f101112130102000102030405060708090a0b0c0d0e0f101112130304abcd0d0a"
        #     ),
        # ]
        # index = 0

        while True:
            try:
                # if index == len(data_sim):
                # break
                received_data = self._connection.recv(1024)
                # received_data = data_sim[index]
                # index += 1

                if not received_data:
                    break

                with self._data_lock:
                    self._data.extend(received_data)
            except socket.error as e:
                print("Socket error: ", e, e.args)

    def __packet_extractor(self):
        # Continuously read from the data queue, extract packets, and remove them
        while True:
            try:
                time.sleep(0.5)

                with self._data_lock:
                    # data = self._data_queue.get()
                    # if not data:
                    #     continue

                    # packets = re.findall(PACKET_REGEX, self._data)
                    packets = self.__extract_all_packets()
                    if not packets:
                        continue

                with self._raw_packets_lock:
                    self._raw_packets.extend(packets)
            except Exception as e:
                print("Error during packet extraction: ", e, e.args)

    def __packet_processor(self):
        while True:
            try:
                time.sleep(0.5)

                with self._raw_packets_lock:
                    parsed_packets = PacketParser(self._raw_packets).parse().get_result()

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
