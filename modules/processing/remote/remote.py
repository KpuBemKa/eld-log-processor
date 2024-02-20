import requests

from modules.models.packet.packet import PacketModel

REMOTE_LINK = "https://dev.hgrs.us/api/system/monitoring/v1/log/"


class Remote:
    _result: dict = {}

    def __init__(self) -> None:
        pass

    def construct_from_packet(self, packet: PacketModel, event_type, event_code) -> "Remote":
        return self.construct_data(
            device_id=packet.header.device_id,
            event_type=event_type,
            event_code=event_code,
            device_timestamp=self.__get_packet_timestamp(packet),
            mileage=self.__get_packet_mileage(packet),
            latitude=self.__get_packet_longitude(packet),
            longitude=self.__get_packet_latitude(packet),
        )

    def construct_data(
        self,
        device_id,
        event_type,
        event_code,
        device_timestamp,
        mileage,
        latitude,
        longitude,
    ) -> "Remote":
        self._result = {
            "device_id": device_id,
            "event_type": event_type,
            "event_code": event_code,
            "timestamp": device_timestamp,
            "accumulated_miles": mileage,
            "accumulated_hours": 1,
            "latitude": latitude,
            "longitude": longitude,
            "malfunction_status": 0,
            "diagnostic_indicator": 0,
        }
        return self

    def send(self):
        requests.post(
            REMOTE_LINK,
            data=self._result,
            verify=False,
        )
        print("Sending data to database:\n", self._result)

    def __get_packet_timestamp(self, packet):
        if "stat_data" in packet["payload"]:
            return packet.payload["stat_data"]["UTC_Time"]

        if "UTC_Time" in packet["payload"]:
            return packet.payload["UTC_Time"]

        return None

    def __get_packet_mileage(self, packet):
        if "stat_data" in packet["payload"]:
            return packet.payload["stat_data"]["current_trip_mileage"]

        return None

    def __get_packet_latitude(self, packet):
        return self.__get_packet_geo(packet, "latitude")

    def __get_packet_longitude(self, packet):
        return self.__get_packet_geo(packet, "longitude")

    def __get_packet_geo(self, packet: PacketModel, param: str) -> dict | None:
        if packet.header.protocol_id == "4009":
            if "gps_item" in packet.payload:
                return packet.payload["gps_item"][param]

        if "gps_data" in packet.payload:
            return packet.payload["gps_data"]["gps_data"][0][param]

        return None
