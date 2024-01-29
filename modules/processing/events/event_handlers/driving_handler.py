from .base_handler import BaseHandler

from modules.processing.redis.redis_realtime import RedisRealtime

DRIVING_THRESHOLD = 8  # km/h = 5 mph
KEY_HEADER = "is_driving"


class DrivingHandler(BaseHandler):
    _redis = RedisRealtime()

    def handle(self, data) -> None:
        self._data = data

        if not self.__is_alarm_packet():
            return

        is_speeding = self.__is_speeding_raised()
        if is_speeding is None:
            return

        message = self.__make_message()
        print("New driving state:\n", message)

    def __is_alarm_packet(self):
        return self._data["header"]["protocol_id"] == "4007"

    def __is_speeding_raised(self):
        for alarm_data in self._data["payload"]["alarm_data"]:
            if alarm_data.alarm_type != "Speeding":
                continue

            return alarm_data.new_alarm_flag == "new alert"

        return None

    def __make_message(self, is_speeding):
        timestamp = self._data["payload"]["stat_data"]["UTC_Time"]
        device_id = self._data["header"]["device_id"]

        return {}.extend([timestamp.__dict__, device_id.__dict__, is_speeding.__dict__])
