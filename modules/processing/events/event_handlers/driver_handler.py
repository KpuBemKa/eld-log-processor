from .base_handler import BaseHandler

from modules.processing.redis.redis_realtime import RedisRealtime

KEY_HEADER = "current_driver"


class DriverAssignmentHandler(BaseHandler):
    _redis = RedisRealtime()

    def handle(self, data) -> None:
        self._data = data

        driver_id = self.__get_driver_id()        
        if not driver_id:
            return

        device_id = self._data["header"]["device_id"]
        if not self.__has_driver_changed(device_id, driver_id):
            return
        
        print("EVENT: Driver", driver_id, "has been assigned to", device_id)
        
    def __get_driver_id(self):
        protocol_id = self._data["header"]["protocol_id"]
        
        if protocol_id == "400C":
            return self._data["payload"]["card_id"]
        
        if protocol_id == "400D":
            return self._data["payload"]["ic_data"]
        
        return None

    def __has_driver_changed(self, device_id, driver_id):
        last_device_driver = self._redis.get_key(KEY_HEADER + ":" + device_id)
        
        return last_device_driver != driver_id
        
