# from modules.processing.persist.persistence import Persistence
from modules.models.packet.packet import PacketModel
from modules.processing.redis.redis_realtime import RedisRealtime
from modules.processing.remote.remote import Remote


REDIS_HEADER = "eld:vstate"
VEHICLE_ERR_EVENT_TYPE = 7


class VehicleErrorHandler:
    _redis = RedisRealtime()

    def handle(self, data: PacketModel) -> None:
        self._data = data

        if not self.__does_packet_have_vstatus():
            return

        stored_vstate = self.__get_stored_vstate(device_id=self._data.header.device_id)
        packet_vstate = self.__get_packet_vstate()

        if self.__are_vstates_equal(stored_vstate, packet_vstate):
            return

        self.__update_stored_vstate(packet_vstate)

        event_code = self.__get_event_code(stored_vstate, packet_vstate)

        if not event_code:
            print("UNKNOWN EVENT CODE FOR VSTATE")
            return

        Remote().construct_from_packet(
            packet=data, event_type=VEHICLE_ERR_EVENT_TYPE, event_code=event_code
        ).send()

    def __does_packet_have_vstatus(self) -> bool:
        if "stat_data" not in self._data.payload:
            return False

        return "vstate" in self._data.payload["stat_data"]

    def __get_stored_vstate(self, device_id) -> dict[str, int]:
        return self._redis.get_key(REDIS_HEADER + ":" + device_id) # type: ignore

    def __get_packet_vstate(self) -> dict[str, int]:
        return self._data.payload["stat_data"]["vstate"]

    def __are_vstates_equal(self, vstate1: dict, vstate2: dict) -> bool:
        return vstate1 == vstate2

    def __update_stored_vstate(self, new_value: dict) -> None:
        self._redis.set_key(REDIS_HEADER + ":" + self._data.header.device_id, new_value)

    def __get_event_code(self, stored_vstate: dict, packet_vstate: dict) -> int | None:
        for id in stored_vstate:
            if stored_vstate[id] == packet_vstate[id]:
                continue

            if int(packet_vstate[id]) == 1:
                return 1
            elif int(packet_vstate[id]) == 0:
                return 0
            else:
                return None
