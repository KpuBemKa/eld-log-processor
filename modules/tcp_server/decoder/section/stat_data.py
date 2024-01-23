from modules.tcp_server.decoder.decoder import Decoder
from modules.tcp_server.models.stat_data import StatData
from modules.tcp_server.enums.stat_data_reserved import StatDataReservedEnum


class StatDataDecoder(Decoder):

    def __init__(self, data, start = 0):
        self.model = StatData()
        self.data = data[start:]


    def decode(self):
        (self.last_accon_time()
         .UTC_Time()
         .total_trip_mileage()
         .current_trip_mileage()
         .total_fuel()
         .current_fuel()
         .vstate()
         .reserved())
        return self

    def last_accon_time(self):
        self.model.set(
            'last_accon_time',
            self.set_part(self.data[:4]).to_hex().reverse_bytes().hex_int().get_part()
        )
        return self

    def UTC_Time(self):
        self.model.set(
            'UTC_Time',
            self.set_part(self.data[4:8]).to_hex().reverse_bytes().hex_int().get_part()
        )
        return self

    def total_trip_mileage(self):
        self.model.set(
            'total_trip_mileage',
            self.set_part(self.data[8:12]).to_hex().reverse_bytes().hex_int().get_part()
        )
        return self

    def current_trip_mileage(self):
        self.model.set(
            'current_trip_mileage',
            self.set_part(self.data[12:16]).to_hex().reverse_bytes().hex_int().get_part()
        )
        return self

    def total_fuel(self):
        self.model.set(
            'total_fuel',
            self.set_part(self.data[16:20]).to_hex().reverse_bytes().hex_int().get_part()
        )
        return self

    def current_fuel(self):
        self.model.set(
            'current_fuel',
            self.set_part(self.data[20:22]).to_hex().reverse_bytes().hex_int().get_part()
        )
        return self

    def vstate(self):
        result = {}

        stage = self.set_part(self.data[22:23]).to_hex().hex_int().to_bin().get_part()
        params = {
            0: 'exhaust_emission',
            1: 'idle_engine',
            2: 'hard_deceleration',
            3: 'hard_acceleration',
            4: 'high_engine_coolant_temperature',
            5: 'speeding',
            6: 'towing',
            7: 'low_voltage'
        }
        result.update(self.vstate_setter(params, stage))

        stage = self.set_part(self.data[23:24]).to_hex().hex_int().to_bin().get_part()
        params = {
            0: 'tamper',
            1: 'crash',
            2: 'emergency',
            3: 'fatigue_driving',
            4: 'sharp_turn',
            5: 'quick_lane_change',
            6: 'power_on',
            7: 'high_rpm'
        }
        result.update(self.vstate_setter(params, stage))

        stage = self.set_part(self.data[24:25]).to_hex().hex_int().to_bin().get_part()
        params = {
            0: 'mil',
            1: 'pull_out/rollover',
            2: 'power-off',
            3: 'no_gps_device',
            4: 'gps_antenna_alarm',
            5: 'ignition_on',
            6: 'illegal_ignition',
            7: 'illegal_enter'
        }
        result.update(self.vstate_setter(params, stage))

        stage = self.set_part(self.data[24:25]).to_hex().hex_int().to_bin().get_part()
        params = {
            0: 'reserved',
            1: 'temperature',
            2: 'door_2_state',
            3: 'door_1_state',
            4: 'vibration',
            5: 'dangerous_driving',
            6: 'no_card_presented',
            7: 'unlock'
        }
        result.update(self.vstate_setter(params, stage))

        self.model.set(
            'vstate',
            result
        )

        return self

    def vstate_setter(self, items, stage):
        result = {}
        for index in items:
            result[items[index]] = stage[index]

        return result

    def reserved(self):
        result = {
            'engine_diagnose_protocol': StatDataReservedEnum().get_engine_diagnose_protocol(
                self.set_part(self.data[26:27]).to_hex().get_part()
            ),
            'vehicle_voltage': self.set_part(self.data[27:28]).to_hex().hex_int().get_part() * 0.1 + 8,
            'network_frequency': StatDataReservedEnum().get_network_frequency(
                self.set_part(self.data[26:27]).to_hex().get_part()
            ),
            'hardware_code': self.set_part(self.data[29:30]).to_hex().get_part()[0],
            'cellular_module_code': self.set_part(self.data[29:30]).to_hex().get_part()[1],
            'cellular_signal-strength': self.set_part(self.data[30:31]).to_hex().get_part(),
            'ber_of_cellular_communication': self.set_part(self.data[31:32]).to_hex().get_part(),
            'system_status_indication': self.set_part(self.data[32:34]).to_hex().get_part(),

        }

    def get_position(self):
        return 34
