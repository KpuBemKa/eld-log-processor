# from modules.processing.persist.persistence import Persistence
from modules.models.packet.packet import PacketModel
from modules.processing.remote.remote import Remote
from modules.processing.redis.redis_realtime import RedisRealtime


REDIS_HEADER = "eld:eld_state"
ELD_ERR_EVENT_TYPE = None


class EldErrorHandler:
    _redis = RedisRealtime()

    def handle(self, data: PacketModel) -> None:
        self._data = data

        if not self.__does_packet_have_eld_state():
            return
        
        return

        stored_eld_state = self.__get_stored_eld_state(device_id=self._data.header.device_id)
        packet_eld_state = self.__get_packet_eld_state()

        if self.__are_eld_states_equal(stored_eld_state, packet_eld_state):
            return

        self.__update_stored_eld_state(packet_eld_state)

        event_code = self.__get_event_code(stored_eld_state, packet_eld_state)

        if not event_code:
            print("UNKNOWN EVENT CODE FOR VSTATE")
            return

        Remote().construct_from_packet(
            packet=data, event_type=ELD_ERR_EVENT_TYPE, event_code=event_code
        ).send()

    def __does_packet_have_eld_state(self) -> bool:
        return False

        if "stat_data" not in self._data["payload"]:
            return False

        return "vstate" in self._data.payload["stat_data"]

    def __get_stored_eld_state(self, device_id):
        return self._redis.get_key(REDIS_HEADER + ":" + device_id)

    def __get_packet_eld_state(self):
        return None
        return self._data.payload["stat_data"]["vstate"]

    def __are_eld_states_equal(self, vstate1: dict, vstate2: dict):
        return vstate1 == vstate2

    def __update_stored_eld_state(self, new_value: dict) -> None:
        self._redis.set_key(REDIS_HEADER + ":" + self._data.header.device_id, new_value)

    def __get_event_code(self, stored_vstate: dict, packet_vstate: dict) -> bool | None:
        return None

        for id in stored_vstate:
            if stored_vstate[id] == packet_vstate[id]:
                continue

            if int(packet_vstate[id]) == 1:
                return 1
            elif int(packet_vstate[id]) == 0:
                return 0
            else:
                return None
