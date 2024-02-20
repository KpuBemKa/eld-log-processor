from modules.decoding.decoder import Decoder
from modules.models.protocols.gps_model import GPS_Model


class GPSDataDecoder(Decoder):
    def __init__(self, data, start=0):
        self.model = GPS_Model()
        self.data = data[start:]
        self.position = 0

    def decode(self):
        self.gps_count().gps_data()
        return self

    def gps_count(self):
        self.model.gps_count = (
            self.set_part(self.data[0 : self.move(1)]).to_hex().hex_int().get_part()
        )
        return self

    def gps_data(self):
        for _ in range(self.model.gps_count):
            data = self.data[self.position : self.position + 20]

            model = self.model.new_gps_data()

            model.date = {
                "day": self.set_part(data[:1]).to_hex().hex_int().get_part(),
                "month": self.set_part(data[1:2]).to_hex().hex_int().get_part(),
                "year": self.set_part(data[2:3]).to_hex().hex_int().get_part() + 2000,
            }

            model.time = {
                "hour": self.set_part(data[3:4]).to_hex().hex_int().get_part(),
                "minute": self.set_part(data[4:5]).to_hex().hex_int().get_part(),
                "second": self.set_part(data[5:6]).to_hex().hex_int().get_part(),
            }
            model.latitude = (
                self.set_part(data[6:10]).to_hex().reverse_bytes().hex_int().get_part() / 3600000
            )
            model.longitude = (
                self.set_part(data[10:14]).to_hex().reverse_bytes().hex_int().get_part() / 3600000
            )
            model.speed = (
                self.set_part(data[14:16]).to_hex().reverse_bytes().hex_int().get_part() * 0.022369
            )
            model.direction = (
                self.set_part(data[16:18]).to_hex().reverse_bytes().hex_int().get_part()
            )
            model.flag = self.gps_flag(self.set_part(data[18:19]).to_hex().get_part())
            self.model.add_gps_data(model.__dict__)

            self.move(19)
        return self

    def gps_flag(self, hex_val):
        flags = self.set_part(hex_val).hex_int().to_bin().get_part().zfill(4)
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
