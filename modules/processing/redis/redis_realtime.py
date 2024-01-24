from .redis_main import RedisMain
import json


class RedisRealtime(RedisMain):
    data = None

    def process(self, data):
        self.data = data
        if "gps_data" in self.data["payload"]:
            self.set_gps_data()

    def set_gps_data(self):
        self.chanel_push(
            "eld:realtime:gps:" + self.data["payload"]["device_id"],
            json.dumps(self.data["payload"]["gps_data"]["gps_data"]),
        )
