import sched
import time

from modules.singleton_meta import SingletonMeta

from modules.processing.redis.redis_main import RedisMain
from modules.processing.storage.gps_handler import GPS_DATA_HEADER


class ScheduleManager(metaclass=SingletonMeta):
    _redis = RedisMain()

    _tasks = []
    _scheduler = sched.scheduler(time.monotonic, time.sleep)

    def add_task(self, task_name:str, time_delay: float, executor: callable[[tuple], None], args: tuple):
        pass

    def add_device_id(self, device_id):
        """
        schedule a task to send device's latest gps data to the server after a delay of an hour
        """
        self._tasks.append(
            {
                "device_id": device_id,
                "task": self._scheduler.enter(3600, 5, self.__send_inter_log, argument=device_id),
            }
        )

    def remove_device_id(self, device_id):
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
        gps_data = self._redis.get_key(GPS_DATA_HEADER + ":" + device_id)

        # schedule to send one more after an hour
        self.add_device_id(device_id)

        # PLACEHOLDER
        print(f"Sending inter log for device_id:{device_id} to server: {gps_data}")

        # Persistence(data).populate(EVENT_TYPE, self.__get_event_code(new_status)).send()
