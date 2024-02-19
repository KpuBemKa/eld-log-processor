from ..decoder import Decoder
from ..section.stat_data import StatDataDecoder
from modules.models.enums.dtc_data.fault_flag import DTCFaultFlagEnum
from modules.models.enums.dtc_data.dtc_attr import DTCAttrEnum

from modules.models.protocols.model_400B import Protocol400BModel


class Protocol400BDecoder(Decoder):
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.result = {}
        self.model = Protocol400BModel()

    def decode(self):
        self.stat_data().protocol_data()
        return self

    def stat_data(self):
        data = StatDataDecoder(self.data, self.position).decode()
        self.position += data.get_position()
        self.result.update({"stat_data": data.get_model()})

        return self

    def protocol_data(self):
        self.model.fault_flag = DTCFaultFlagEnum().get(
            self.set_part(self.data[self.position : self.move(1)]).to_hex().hex_int().get_part()
        )
        self.model.fault_count = (
            self.set_part(self.data[self.position : self.move(1)]).to_hex().hex_int().get_part()
        )

        for _ in range(self.model.fault_count):
            model = self.model.getDTC_Model()
            model.code = self.data[self.position : self.move(2)]

            attr = (
                self.set_part(self.data[self.position : self.move(1)]).to_hex().to_bin().get_part()
            )
            attr = str(attr[4]) + str(attr[3]) + str(attr[2]) + str(attr[1]) + str(attr[0])
            attr = self.set_part(attr).hex_int(2).get_part()

            model.attr = DTCAttrEnum().get(attr)

            self.model.add_fault(model.__dict__)

        self.model.mil_status = self.data[self.position, self.move(2)]

        return self

    def get_result(self):
        return self.result
