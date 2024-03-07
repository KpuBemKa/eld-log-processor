from modules.decoding.decoder import Decoder
from modules.decoding.section.gps_data import GPSDataDecoder
from modules.models.protocols.model_4009 import Protocol4009Model


class Protocol4009Decoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}
        self.model = Protocol4009Model()

    def decode(self):
        self.protocol_data().gps_data()
        return self

    def protocol_data(self):
        self.model.utc_time = int.from_bytes(
            self.data[self.position : self.move(4)], byteorder="little"
        )

        return self

    def gps_data(self):
        data = GPSDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.model.gps_item.update({"gps_data": data.get_model()})

        return self

    def get_result(self):
        return self.model.__dict__
