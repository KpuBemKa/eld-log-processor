from .base_handler import BaseHandler

from modules.processing.redis.redis_realtime import RedisRealtime
from modules.processing.persist.persistence import Persistence


KEY_HEADER = "is_engine_running"
EVENT_TYPE = 6


class DrivingHandler(BaseHandler):
    _redis = RedisRealtime()

    def handle(self, data) -> None:
        self._data = data

        if not self.__is_alarm_packet():
            return

        is_ignition_on = self.__is_ignition_on()
        if is_ignition_on is None:
            return

        Persistence(data).populate(EVENT_TYPE, self.__get_event_code(is_ignition_on)).send()

    def __is_alarm_packet(self):
        return self._data["header"]["protocol_id"] == "4007"

    def __is_ignition_on(self):
        for alarm_data in self._data["payload"]["alarm_data"]:
            if alarm_data.alarm_type == "Ignition on":
                return True

            if alarm_data.alarm_type == "Ignition off":
                return False

        return None

    def __get_event_code(self, is_ignition_on):
        # location precision should always be maximum
        if is_ignition_on:
            return 1 # Engine power-up with conventional location precision
        else:
            return 3 # Engine shut-down with conventional location precision

    # def __make_message(self, is_ignition_on):
    #     if "GPS_Data" in self._data["payload"]:
    #         gps_data = self._data["payload"]["stat_data"]["GPS_Data"]
    #     else:
    #         gps_data = ""

    #     device_id = self._data["header"]["device_id"]

    #     return {}.extend([device_id.__dict__, is_ignition_on.__dict__, gps_data.__dict__])
