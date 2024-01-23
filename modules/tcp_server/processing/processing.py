from .redis.redis_realtime import RedisRealtime
from .socketio.socketio_realtime import SoketioRealtime
from modules.tcp_server.processing.persist.persistence import Persistence


class Processing:
    data = None

    def __init__(self, data):
        self.data = data

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

    def process(self):
        self.realtime_data()
        self.storage_data()
        self.persist_data()

    def additional_check(self):
        return self.vin_check()

    def vin_check(self):
        if "device_id" not in self.data["payload"]:
            return False

        if self.data["payload"]["device_id"] is None:
            return False

        return True
