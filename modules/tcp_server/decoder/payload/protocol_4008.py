from ..decoder import Decoder
from modules.tcp_server.models.protocol_4001 import Protocol4001Model
from modules.tcp_server.models.protocol_4008 import Protocol4008Model

from ..section.stat_data import StatDataDecoder
from ..section.gps_data import GPSDataDecoder
from ..section.alarm_data import AlarmDataDecoder


class Protocol4008Decoder(Decoder):

    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}
        self.model = Protocol4008Model()


    def decode(self):
        self.stat_data().protocol_data()
        return self

    def stat_data(self):
        data = StatDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({'stat_data': data.get_model()})

        return self

    def protocol_data(self):
        self.model.local_area_code = self.set_part(self.data[self.position: self.move(2)]).to_hex().reverse_bytes().get_result()
        self.model.cell_id = self.set_part(self.data[self.position: self.move(2)]).to_hex().reverse_bytes().get_result()

        self.result.update(self.model.__dict__)

        return self

    def get_result(self):
        return self.result
