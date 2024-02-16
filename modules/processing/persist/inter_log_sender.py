import sched
import time

from modules.singleton_meta import SingletonMeta

from modules.processing.redis.redis_main import RedisMain
from modules.processing.storage.gps_handler import GPS_DATA_HEADER


class InterLogSender(metaclass=SingletonMeta):
    _redis = RedisMain()

    _tasks = []
    _scheduler = sched.scheduler(time.monotonic, time.sleep)

    def __init__(self) -> None:
        pass

    def add_device_id(self, device_id):
        self._tasks.append(
            {
                "device_id": device_id,
                "task": self._scheduler.enter(3600, 5, self.__send_inter_log, argument=device_id),
            }
        )

    def remove_device_id(self, device_id):
        for task in self._tasks:
            if task["device_id"] == device_id:
                self._scheduler.cancel(task["task"])

    def __send_inter_log(self, device_id):
        gps_data = self._redis.get_key(GPS_DATA_HEADER + ":" + device_id)

        print(f"Sending inter log for device_id:{device_id} to server: {gps_data}")

        # Persistence(data).populate(EVENT_TYPE, self.__get_event_code(new_status)).send()
