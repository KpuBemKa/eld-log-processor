from modules.models.packet.packet import PacketModel

from .response_1001 import Main1001Response
from .response_C007 import MainC007Response
from .response_C00C import MainC00CResponse
from .response_C00D import MainC00DResponse

from .request_2001 import Request2001
from .request_2002 import Request2002
from .header import HeaderResponse


class Response:
    _packet: PacketModel
    
    def __init__(self, data: PacketModel):
        self._packet = data

    def make(self):
        match self._packet.header.protocol_id:
            case "1001":
                payload = Main1001Response().make()
                return HeaderResponse(self._packet).make(payload, "9001")

            case "1003":
                return HeaderResponse(self._packet).make(b"", "9003")

            case "4007":
                payload = MainC007Response(self._packet).make()
                return HeaderResponse(self._packet).make(payload, "C007")

            case "400c":
                payload = MainC00CResponse(self._packet).make()
                return HeaderResponse(self._packet).make(payload, "C00C")

            case "400d":
                payload = MainC00DResponse(self._packet).make()
                return HeaderResponse(self._packet).make(payload, "C00D")

        return None

    def make_request(self, protocol_id):
        match protocol_id:
            case "2002":
                payload = Request2002().make()
                return HeaderResponse(self._packet).make(payload, "2002")

            case "2001":
                payload = Request2001().make()
                return HeaderResponse(self._packet).make(payload, "2001")

        return None
