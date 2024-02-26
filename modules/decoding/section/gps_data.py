import struct
from modules.decoding.decoder import Decoder
from modules.models.protocols.gps_model import GPS_Model


# https://docs.python.org/3/library/struct.html
GPS_UNPACK_STR = "<" + "BBB" + "BBB" + "II" + "H" + "H" + "B"


class GPSDataDecoder(Decoder):
    model: GPS_Model
    data: bytes
    position: int

    def __init__(self, data, start=0):
        self.model = GPS_Model()
        self.data = data[start:]
        self.position = 0

    def decode(self) -> "GPSDataDecoder":
        self.gps_count().gps_data()
        return self

    def gps_count(self) -> "GPSDataDecoder":
        self.model.gps_count = int.from_bytes(self.data[0 : self.move(1)], byteorder="little")
        return self

    def gps_data(self):
        for _ in range(self.model.gps_count):
            raw_data = self.data[self.position : self.position + 20]

            (
                day,
                month,
                year,
                hour,
                minute,
                second,
                latitude,
                longitude,
                speed,
                direction,
                flag,
            ) = self.__unpack(raw_data)

            model = self.model.new_gps_data()

            model.date = {
                "day": day,
                "month": month,
                "year": year,
            }
            model.time = {
                "hour": hour,
                "minute": minute,
                "second": second,
            }

            model.latitude = latitude / 3600000
            model.longitude = longitude / 3600000

            model.speed = speed * 0.022369

            model.direction = direction

            model.flag = self.gps_flag(flag)

            self.model.add_gps_data(model.__dict__)

            self.move(19)
        return self

    def gps_flag(self, flag: int):
        # int -> string binary representation -> strip leading '0b' ->
        # fill the string to have 8 symbols -> reverse the string
        flags = bin(flag)[2:].zfill(8)[::-1]
        response = {}

        if flags[0] == "1":
            response["longitude"] = "east"

        if flags[0] == "0":
            response["longitude"] = "west"

        if flags[1] == "1":
            response["latitude"] = "north"

        if flags[1] == "0":
            response["latitude"] = "south"

        if flags[2] + flags[3] == "00":
            response["fix"] = "No fix"

        if flags[2] + flags[3] == "01":
            response["fix"] = "2D fix"

        if flags[2] + flags[3] == "11":
            response["fix"] = "3D fix"

        return response

    def get_position(self):
        return self.position

    def __unpack(self, raw_data) -> tuple[int, int, int, int, int, int, int, int, int, int, int]:
        return struct.unpack(GPS_UNPACK_STR, raw_data)
