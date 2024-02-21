import struct
from modules.decoding.decoder import Decoder
from modules.models.enums.stat_data_reserved import StatDataReservedEnum
from modules.models.protocols.stat_data import StatData


# https://docs.python.org/3/library/struct.html
STAT_UNPACK_STR = "<" + "II" + "II" + "IH" + "I" + "8s"

VSTATE_PARAMS = [
    "low_voltage",  # 0
    "towing",  # 1
    "speeding",  # 2
    "high_engine_coolant_temperature",  # 3
    "hard_acceleration",  # 4
    "hard_deceleration",  # 5
    "idle_engine",  # 6
    "exhaust_emission",  # 7
    #
    "high_rpm",  # 0
    "power_on",  # 1
    "quick_lane_change",  # 2
    "sharp_turn",  # 3
    "fatigue_driving",  # 4
    "emergency",  # 5
    "crash",  # 6
    "tamper",  # 7
    #
    "illegal_enter",  # 0
    "illegal_ignition",  # 1
    "ignition_on",  # 2
    "gps_antenna_alarm",  # 3
    "no_gps_device",  # 4
    "power-off",  # 5
    "pull_out/rollover",  # 6
    "mil",  # 7
    #
    "reserved",  # 0
    "temperature",  # 1
    "door_2_state",  # 2
    "door_1_state",  # 3
    "vibration",  # 4
    "dangerous_driving",  # 5
    "no_card_presented",  # 6
    "unlock",  # 7
]


class StatDataDecoder(Decoder):
    def __init__(self, data, start=0):
        self.model = StatData()
        self.data = data[start:]

    def decode(self):
        (
            last_accon_time,
            utc_time,
            total_trip_mileage,
            current_trip_mileage,
            total_fuel,
            current_fuel,
            vstate,
            reserved,
        ) = struct.unpack(STAT_UNPACK_STR, self.data)

        self.model.last_accon_time = last_accon_time
        self.model.utc_time = utc_time
        self.model.total_trip_mileage = total_trip_mileage
        self.model.current_trip_mileage = current_trip_mileage
        self.model.total_fuel = total_fuel
        self.model.current_fuel = current_fuel
        self.model.vstate = self.__parse_vstate(vstate)
        self.model.reserved = self.__parse_reserved(reserved)

        return self

    def __parse_reserved(self, values: bytes) -> dict[str, str]:
        return {
            "engine_diagnose_protocol": StatDataReservedEnum().get_engine_diagnose_protocol(
                values[0]
            ),
            "vehicle_voltage": str(values[1]),
            "network_frequency": StatDataReservedEnum().get_network_frequency(values[2]),
            "hardware_code": str((values[3] & (0b11110000)) >> 4),  # higher 4 bits
            "cellular_module_code": str(values[3] & (0b00001111)),  # lower 4 bits,
            "cellular_signal-strength": str(values[4]),
            "ber_of_cellular_communication": str(values[5]),
            "system_status_indication": values[-2:].hex(), # last 2 bytes
        }

    def __parse_vstate(self, vstate: int) -> dict[str, bool]:
        result: dict[str, bool] = {}

        i = 0
        for param in VSTATE_PARAMS:
            result[param] = bool(self.__get_bit(vstate, i))
            i += 1

        return result

    def __get_bit(self, source: int, position: int):
        return source & (1 << position)
