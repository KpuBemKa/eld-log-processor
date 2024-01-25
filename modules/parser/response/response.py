from .main_1001 import Main1001Response
from .main_C007 import MainC007Response
from .request_2002 import Request2002
from .header import HeaderResponse


class Response:
    def __init__(self, connection, data):
        self.data = data
        self.connection = connection

    def make(self):
        match self.data["header"]["protocol_id"]:
            case "1001":
                payload = Main1001Response(self.connection).make()
                return HeaderResponse(self.data).make(payload, "9001")

            case "1003":
                return HeaderResponse(self.data).make(b"", "9003")

            case "4007":
                payload = MainC007Response(self.data).make()
                return HeaderResponse(self.data).make(payload, "C007")

    def make_request(self, protocol):
        match protocol:
            case "2002":
                payload = Request2002().make()
                return HeaderResponse(self.data).make(payload, "2002")
