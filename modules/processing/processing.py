from .redis.redis_realtime import RedisRealtime

# from .socketio.socketio_realtime import SoketioRealtime
from modules.processing.persist.persistence import Persistence

from .events.events import EventsProcessor


class Processing:
    _events_processor = EventsProcessor()
    data = None

    def __init__(self):
        pass

    def process(self, data):
        self.data = data

        self.realtime_data()
        self.storage_data()
        self.persist_data()
        self.events_data()

    def realtime_data(self):
        RedisRealtime().process(self.data)

    def storage_data(self):
        pass

    def persist_data(self):
        if (
            self.data["header"]["protocol_id"] == "4001"
            or self.data["header"]["protocol_id"] == "4009"
        ):
            Persistence(self.data).populate().send()

    def additional_check(self, data):
        self.data = data

        return self.vin_check()

    def vin_check(self):
        if "device_id" not in self.data["header"]:
            return False

        if self.data["header"]["device_id"] is None:
            return False

        return True

    def events_data(self):
        self._events_processor.process(self.data)
