from modules.models.packet.packet import PacketModel


class MainC007Response:
    response = {}

    def __init__(self, data: PacketModel):
        self.data = data

    def make(self):
        return self.data.payload["alarm_seq"]
