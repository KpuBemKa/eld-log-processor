from modules.decoder.decoder import Decoder
from modules.models.alarm_model import Alarm_Model
from modules.enums.alarm_data.new_alarm_flag import AlarmNewFlagEnum
from modules.enums.alarm_data.alarm_type import AlarmTypeEnum


class AlarmDataDecoder(Decoder):
    def __init__(self, data, start=0):
        self.model = Alarm_Model()
        self.data = data[start:]
        self.position = 0

    def decode(self):
        self.alarm_count().alarm_data()
        return self

    def alarm_count(self):
        self.model.alarm_count = (
            self.set_part(self.data[0 : self.move(1)]).to_hex().hex_int().get_part()
        )
        return self

    def alarm_data(self):
        for _ in range(self.model.alarm_count):
            model = self.model.new_alarm_data()

            model.new_alarm_flag = AlarmNewFlagEnum().get(
                self.set_part(self.data[self.position : self.move(1)])
                .to_hex()
                .get_part()
            )
            model.alarm_type = AlarmTypeEnum().get(
                self.set_part(self.data[self.position : self.move(1)])
                .to_hex()
                .get_part()
            )
            model.alarm_description = (
                self.set_part(self.data[self.position : self.move(2)])
                .to_hex()
                .reverse_bytes()
                .get_part()
            )
            model.alarm_threshold = (
                self.set_part(self.data[self.position : self.move(2)])
                .to_hex()
                .reverse_bytes()
                .get_part()
            )

            self.model.add_alarm_data(model.__dict__)

        return self

    def get_model(self):
        return self.model

    def get_position(self):
        return self.position
