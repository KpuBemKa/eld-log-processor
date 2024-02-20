from modules.models.packet.packet import PacketModel


class MainC00CResponse:
    def __init__(self, data: PacketModel):
        self.data = data

    def make(self):
        return self.data.payload["card_id"]
