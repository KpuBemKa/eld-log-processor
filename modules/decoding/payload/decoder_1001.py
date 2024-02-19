from ..decoder import Decoder
from ..section.stat_data import StatDataDecoder
from ..section.gps_data import GPSDataDecoder

from modules.models.protocols.model_1001 import Protocol1001Model


class Protocol1001Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}

    def decode(self):
        self.stat_data().gps_data().protocol_data()
        return self

    def stat_data(self):
        data = StatDataDecoder(self.data).decode()
        self.position += data.get_position()
        self.result.update({"stat_data": data.get_model()})
        return self

    def gps_data(self):
        data = GPSDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({"gps_data": data.get_model()})
        return self

    def protocol_data(self):
        data = Protocol1001Model()
        data.software_version = self.data[self.position : self.move(32)]
        data.hardware_version = self.data[self.position + 32 : self.move(64)]
        data.hardware_version = self.data[self.position + 64 : self.move(66)]
        self.result.update(data.__dict__)

        return self

    def get_result(self):
        return self.result

    # def __init__(self, data):
    #     self.data = data
    #     self.position = 35
    #     self.model = Protocol1001Model()
    #
    # def decode(self):
    #     return self.gps_count().gps_data().last_data()
    #
    # def gps_count(self):
    #     self.model.gps_count = self.set_part(self.data[34:35]).to_hex().hex_int().get_part()
    #     return self
    #
    # def last_data(self):
    #     self.model.software_version = self.data[self.position : self.position + 32]
    #     self.model.hardward_version = self.data[self.position + 32 : self.position + 64]
    #     self.model.hardward_version = self.data[self.position + 64 : self.position + 66]
    #
    #     return self
    #
    # def gps_data(self):
    #     for i in range(self.model.gps_count):
    #         gps = GPS_Model()
    #         data = self.data[self.position: self.position + 20]
    #
    #         gps.date = {
    #             'day': self.set_part(data[:1]).to_hex().hex_int().get_part(),
    #             'month': self.set_part(data[1:2]).to_hex().hex_int().get_part(),
    #             'year': self.set_part(data[2:3]).to_hex().hex_int().get_part() + 2000
    #         }
    #
    #         gps.time = {
    #             'hour': self.set_part(data[3:4]).to_hex().hex_int().get_part(),
    #             'minute': self.set_part(data[4:5]).to_hex().hex_int().get_part(),
    #             'second': self.set_part(data[5:6]).to_hex().hex_int().get_part()
    #         }
    #         gps.latitude = self.set_part(data[6:10]).to_hex().reverse_bytes().hex_int().get_part()
    #         gps.longitude = self.set_part(data[10:14]).to_hex().reverse_bytes().hex_int().get_part()
    #         gps.speed = self.set_part(data[14:16]).to_hex().reverse_bytes().hex_int().get_part()
    #         gps.direction = self.set_part(data[16:18]).to_hex().reverse_bytes().hex_int().get_part()
    #         gps.flag = self.gps_flag(self.set_part(data[18:19]).to_hex().get_part())
    #         self.model.add_gps_data(gps.__dict__)
    #
    #         self.position += 19
    #
    #     return self
    #
    # def gps_flag(self, hex):
    #     flags = self.set_part(hex).hex_int().to_bin().get_part().zfill(4)
    #     response = {}
    #
    #     if flags[0] == '1':
    #         response['longitude'] = 'east'
    #
    #     if flags[0] == '0':
    #         response['longitude'] = 'west'
    #
    #     if flags[1] == '1':
    #         response['latitude'] = 'north'
    #
    #     if flags[1] == '0':
    #         response['latitude'] = 'south'
    #
    #     if flags[2] + flags[3] == '00':
    #         response['fix'] = 'No fix'
    #
    #     if flags[2] + flags[3] == '01':
    #         response['fix'] = '2D fix'
    #
    #     if flags[2] + flags[3] == '11':
    #         response['fix'] = '3D fix'
    #
    #     return response
    #
    # def get_model(self):
    #     return self.model.get_data()
