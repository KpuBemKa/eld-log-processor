import calendar

from modules.processing.redis.redis_main import RedisMain

# from ..events.event_handlers.base_handler import BaseHandler
# from modules.processing.events.event_handlers.driver_handler import DriverAssignmentHandler

GPS_DATA_HEADER = "eld:latest_gps_data"
GPS_STAMP_HEADER = "eld:latest_gps_stamp"
EVENT_TYPE = 1


# class GpsHandler(BaseHandler):
class GpsHandler():
    _redis = RedisMain()
    _data = None

    def handle(self, data) -> None:
        self._data = data

        if "gps_data" not in data["payload"]:
            return

        self.__save_latest_gps()

    def __save_latest_gps(self):
        stored_stamp = self.__get_stored_stamp()
        packet_stamp = self.__get_packet_timestamp()

        # if stored timestamp value is bigger, latest gps data is already stored
        if stored_stamp > packet_stamp:
            return

        self.__set_stored_stamp(packet_stamp)
        self.__set_stored_gps(self._data["payload"]["gps_data"])

    def __get_stored_stamp(self) -> int:
        value = self._redis.get_key(GPS_STAMP_HEADER + ":" + self._data["header"]["driver_id"])

        if value:
            return int(value)
        else:
            return 0

    def __get_packet_timestamp(self) -> int:
        if "stat_data" in self._data["payload"]:
            return self._data["payload"]["stat_data"]["UTC_Time"]

        if "UTC_Time" in self._data["payload"]:
            return self._data["payload"]["UTC_Time"]
          
        gps_data = self._data["payload"]["gps_data"]
        return calendar.timegm(
            year=gps_data["date"]["year"],
            month=gps_data["date"]["month"],
            day=gps_data["date"]["day"],
            hour=gps_data["time"]["hour"],
            minute=gps_data["time"]["minute"],
            second=gps_data["time"]["second"],
        )

    def __set_stored_stamp(self, new_stamp):
        return self._redis.set_key(
            GPS_STAMP_HEADER + ":" + self._data["header"]["driver_id"], new_stamp
        )

    def __set_stored_gps(self, new_gps):
        return self._redis.set_key(
            GPS_DATA_HEADER + ":" + self._data["header"]["driver_id"], new_gps
        )
