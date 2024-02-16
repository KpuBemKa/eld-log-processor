import requests

LOG_LINK = "https://dev.hgrs.us/api/system/monitoring/v1/log/"
# LOG = 'https://127.0.0.1:8000/api/system/monitoring/v1/log/'
# ALERT = 'https://127.0.0.1:8000/api/system/monitoring/v1/alert/'


class Persistence:
    result = {}

    def __init__(self, data):
        self.data = data

    def populate(self, event_type, event_code):
        self.result = {
            "device_id": self.data["header"]["device_id"],
            "event_type": event_type,
            "event_code": event_code,
            "timestamp": self.getTimestamp(),
            "accumulated_miles": self.data["payload"]["stat_data"]["current_trip_mileage"],
            "accumulated_hours": 1,
            "latitude": self.getGeo("latitude"),
            "longitude": self.getGeo("longitude"),
            "malfunction_status": 0,
            "diagnostic_indicator": 0,
        }
        return self

    def send(self):
        requests.post(
            LOG_LINK,
            data=self.result,
            verify=False,
        )
        print("Sending data to database:\n", self.result)

    def calculateEventCode(self):
        if self.data["header"]["protocol_id"] == "4009":
            return 1

        if self.data["header"]["protocol_id"] == "4001":
            if self.data["payload"]["gps_data"]["gps_data"][0]["speed"] > 0:
                return 1

            return 4

        return 1

    def calculateEventType(self):
        if self.data["header"]["protocol_id"] == "4009":
            return 1

        if self.data["header"]["protocol_id"] == "4001":
            if self.data["payload"]["gps_data"]["gps_data"][0]["speed"] > 0:
                return 2

            return 1

        return 1

    def getGeo(self, param):
        if self.data["header"]["protocol_id"] == "4009":
            if "gps_item" in self.data["payload"]:
                return self.data["payload"]["gps_item"][param]

        if "gps_data" in self.data["payload"]:
            return self.data["payload"]["gps_data"]["gps_data"][0][param]

        return None

    def getTimestamp(self):
        if "stat_data" in self.data["payload"]:
            return self.data["payload"]["stat_data"]["UTC_Time"]

        if "UTC_Time" in self.data["payload"]:
            return self.data["payload"]["UTC_Time"]
