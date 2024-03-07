""" Alarm data parser """

import struct
from modules.decoding.decoder import Decoder
from modules.models.enums.alarm_data.new_alarm_flag import AlarmNewFlagEnum
from modules.models.enums.alarm_data.alarm_type import AlarmTypeEnum
from modules.models.protocols.alarm_model import Alarm_Model


ALARM_UNPACK_STR = "<" + "BBHH"
DATA_SIZE = 6


class AlarmDataDecoder(Decoder):
    """Alarm data parser"""

    def __init__(self, data: bytes, start=0):
        self.model = Alarm_Model()
        self.data = data[start:]
        self.position = 0

    def decode(self):
        self.alarm_count().alarm_data()
        return self

    def alarm_count(self):
        self.model.alarm_count = self.data[0]
        self.move(1)
        return self

    def alarm_data(self):
        for _ in range(self.model.alarm_count):
            model = self.model.new_alarm_data()

            raw_data = self.data[self.position : self.move(DATA_SIZE)]

            (alarm_flag, alarm_type, alarm_desc, alarm_thr) = struct.unpack(
                ALARM_UNPACK_STR, raw_data
            )

            model.new_alarm_flag = AlarmNewFlagEnum().get(alarm_flag)
            model.alarm_type = AlarmTypeEnum().get(alarm_type)
            model.alarm_description = alarm_desc
            model.alarm_threshold = alarm_thr

            self.model.add_alarm_data(model.__dict__)

        return self

    def get_model(self):
        return self.model

    def get_position(self):
        return self.position
