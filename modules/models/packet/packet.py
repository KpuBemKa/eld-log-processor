from .header import HeaderModel
from .trailer import TrailerModel


class PacketModel:
    header: HeaderModel
    trailer: TrailerModel
    payload: dict

    def __init__(self) -> None:
        self.header = HeaderModel()
        self.trailer = TrailerModel()
        self.payload = {}

    def set(self, param, value):
        setattr(self, param, value)
