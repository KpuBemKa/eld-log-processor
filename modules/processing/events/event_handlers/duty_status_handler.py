from .base_handler import BaseHandler
from modules.enums.duty_status import DutyStatus
from modules.processing.persist.persistence import Persistence
from modules.processing.redis.redis_main import RedisMain
from modules.processing.persist.inter_log_sender import InterLogSender
# from modules.processing.events.event_handlers.driver_handler import DriverAssignmentHandler

STATUS_HEADER = "eld:driver_status"
EVENT_TYPE = 1


class DutyStatusHandler(BaseHandler):
    _redis = RedisMain()
    _data = None

    def handle(self, data) -> None:
        self._data = data

        if not self.__is_status_packet() and not self.__is_alarm_packet():
            return

        device_id = self.__get_device_id()
        last_status = self.__get_last_status(device_id)
        new_status = self.__get_new_status(last_status)

        if new_status == last_status:
            return

        if new_status == DutyStatus.DRIVING:
            self.__start_inter_logging()
        else:
            self.__stop_inter_logging()

        self.__set_last_status(device_id, new_status)

        Persistence(data).populate(EVENT_TYPE, self.__get_event_code(new_status)).send()

    def __is_alarm_packet(self):
        return self._data["header"]["protocol_id"] == "4007"

    def __is_status_packet(self):
        return self._data["header"]["protocol_id"] == "ffff"  # test protocol

    def __is_speeding_raised(self):
        for alarm_data in self._data["payload"]["alarm_data"]:
            if alarm_data.alarm_type != "Speeding":
                continue

            return alarm_data.new_alarm_flag == "new alert"

        return None

    def __get_last_status(self, device_id):
        return self._redis.get_key(STATUS_HEADER + ":" + device_id)

    def __set_last_status(self, device_id, new_status):
        self._redis.set_key(STATUS_HEADER + ":" + device_id, new_status)

    def __get_new_status(self, last_statuts):
        if "duty status" in self._data["payload"]:
            return self._data["payload"]["duty status"]

        if not self.__is_speeding_raised():
            return None

        if last_statuts == DutyStatus.ON_DUTY:
            return DutyStatus.DRIVING
        else:
            return None

    def __get_device_id(self):
        return self._data["header"]["device_id"]

    def __get_event_code(self, new_status):
        match new_status:
            case DutyStatus.OFF_DUTY:
                return 1

            case DutyStatus.SLEEPING:
                return 2

            case DutyStatus.DRIVING:
                return 3

            case DutyStatus.ON_DUTY:
                return 4

            case _:
                return 0

    def __start_inter_logging(self):
        InterLogSender().add_device_id(device_id=self._data["header"]["device_id"])

    def __stop_inter_logging(self):
        InterLogSender().remove_device_id(device_id=self._data["header"]["device_id"])
