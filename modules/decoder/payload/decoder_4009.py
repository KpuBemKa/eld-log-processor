from ..decoder import Decoder
# from modules.models.protocol_4001 import Protocol4001Model
from modules.models.model_4009 import Protocol4009Model
from modules.models.gps_model import GPS_Model

# from ..section.stat_data import StatDataDecoder
# from ..section.gps_data import GPSDataDecoder
# from ..section.alarm_data import AlarmDataDecoder


class Protocol4009Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}
        self.model = Protocol4009Model()

    def decode(self):
        self.protocol_data()
        return self

    def protocol_data(self):
        self.model.UTC_time = (
            self.set_part(self.data[:4]).to_hex().reverse_bytes().hex_int().get_part()
        )
        data = self.data[self.position : self.position + 20]

        model = GPS_Model().new_gps_data()

        model.date = {
            "day": self.set_part(data[self.position : self.move(1)])
            .to_hex()
            .hex_int()
            .get_part(),
            "month": self.set_part(data[self.position : self.move(1)])
            .to_hex()
            .hex_int()
            .get_part(),
            "year": self.set_part(data[self.position : self.move(1)])
            .to_hex()
            .hex_int()
            .get_part()
            + 2000,
        }

        model.time = {
            "hour": self.set_part(data[self.position : self.move(1)])
            .to_hex()
            .hex_int()
            .get_part(),
            "minute": self.set_part(data[self.position : self.move(1)])
            .to_hex()
            .hex_int()
            .get_part(),
            "second": self.set_part(data[self.position : self.move(1)])
            .to_hex()
            .hex_int()
            .get_part(),
        }

        model.longitude = (
            self.set_part(data[self.position : self.move(4)])
            .to_hex()
            .reverse_bytes()
            .hex_int()
            .get_part()
            / 3600000
        )
        model.latitude = (
            self.set_part(data[self.position : self.move(4)])
            .to_hex()
            .reverse_bytes()
            .hex_int()
            .get_part()
            / 3600000
        )
        model.speed = (
            self.set_part(data[self.position : self.move(2)])
            .to_hex()
            .reverse_bytes()
            .hex_int()
            .get_part()
            * 0.022369
        )
        model.direction = (
            self.set_part(data[self.position : self.move(2)])
            .to_hex()
            .reverse_bytes()
            .hex_int()
            .get_part()
        )
        model.flag = self.gps_flag(
            self.set_part(data[self.position : self.move(1)]).to_hex().get_part()
        )

        self.model.gps_item = model.__dict__

        self.result.update(self.model.__dict__)

        return self

    def gps_flag(self, hex):
        flags = self.set_part(hex).hex_int().to_bin().get_part().zfill(4)
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

    def get_result(self):
        return self.result
