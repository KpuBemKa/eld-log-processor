from .redis_main import RedisMain
import json


class RedisRealtime(RedisMain):
    data = None

    def process(self, data):
        self.data = data
        if "gps_data" in self.data["payload"]:
            self.publish_gps_data()

    def publish_gps_data(self):
        self.chanel_push(
            "eld:realtime:gps:" + self.data["header"]["device_id"],
            json.dumps(self.data["payload"]["gps_data"]["gps_data"]),
        )
