"""

TODO event types:
- Driver assignment -> uknown assignment protocol 

- Driver status: [
    Driving,
    On Duty,
    Off Duty,
    Sleeping,
    YM (weather factor),
    PC (personal use),
    PC/YM Cleared
] -> unknown duty status protocol

- ELD malfunction & ELD malfunction cleared -> unknown ELD malfunction protocol


Done but not tested:
- Engine Power-up & Shut-down (always marked as with max location precision)

- Intermediate log once per hour of DRIVING status active
  (always marked as with max location precision)

- Vehicle malfunction & Vehicle malfunction cleared


Done and tested:


"""

# import multiprocessing
# from modules.tcp_server.server import TCPServer


# def main():
#     """Entry point"""

#     server = TCPServer()

#     p = multiprocessing.Process(target=server.run, daemon=True)
#     p.start()
#     p.join()

#     # while True:
#     #     pass


# if __name__ == "__main__":
#     # main()
#     pass

# from modules.decoding.section.gps_data import GPSDataDecoder

# # 09.02.10 | 18:07:13 | 28.3 | 49.52 | 49.99553 | 130 | 0b01001111
# raw_gps_item = (
#     b"\x09\x02\x0A"
#     b"\x12\x07\x0C"
#     b"\xC0\x90\x12\x06"
#     b"\x00\x37\xA0\x0A"
#     b"\xBB\x08"
#     b"\x14\x05"
#     b"\x4f"
# )

# gps_data = b"\x01" + raw_gps_item

# result = GPSDataDecoder(gps_data).decode().get_model()

# from modules.decoding.decoder_header import DecoderHeader

# raw_header = (
#   b"\x40\x40"
#   b"\x1a\x00"
#   b"\x01"
#   b"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x5F\x31\x32\x33\x34\x35\x36\x37\x38\x39"
#   b"\x01\x10"
# )

# print(DecoderHeader(raw_header).decode().get_model().__dict__)


# from modules.decoding.decoder_trailer import TrailerDecoder

# raw_trailer = (
#     b"\x34\x12"  # 4660
#     b"\r\n"
# )

# print(TrailerDecoder(raw_trailer).decode().get_model().__dict__)
