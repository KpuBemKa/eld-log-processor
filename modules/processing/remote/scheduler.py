import sched
import time

from remote import Remote

from modules.singleton_meta import SingletonMeta

from modules.processing.redis.redis_main import RedisMain

from modules.processing.storage.gps_handler import GPS_DATA_HEADER
from modules.processing.storage.gps_handler import GPS_STAMP_HEADER


INTER_LOG_EVENT_TYPE = 2
INTER_LOG_EVENT_CODE = 1


class ScheduleManager(metaclass=SingletonMeta):
    _redis = RedisMain()

    _tasks = []
    _scheduler = sched.scheduler(time.monotonic, time.sleep)

    def add_inter_log_task(self, device_id):
        """
        schedule a task to send device's latest gps data to the server after a delay of an hour
        """
        self._tasks.append(
            {
                "device_id": device_id,
                "task": self._scheduler.enter(3600, 5, self.__send_inter_log, argument=device_id),
            }
        )

    def remove_inter_log_task(self, device_id):
        """
        cancel scheduled task
        """
        for task in self._tasks:
            if task["device_id"] == device_id:
                self._scheduler.cancel(task["task"])

    def __send_inter_log(self, device_id):
        """
        get latest gps data from the redis database, and send it
        """
        # schedule to send one more after an hour
        self.add_inter_log_task(device_id)

        gps_data = self._redis.get_key(GPS_DATA_HEADER + ":" + device_id)
        device_stamp = self._redis.get_key(GPS_STAMP_HEADER + ":" + device_id)

        Remote().construct_data(
            device_id=device_id,
            event_type=INTER_LOG_EVENT_TYPE,
            event_code=INTER_LOG_EVENT_CODE,
            device_timestamp=device_stamp,
            mileage=None,
            latitude=gps_data["latitude"],
            longitude=gps_data["longitude"],
        ).send()
