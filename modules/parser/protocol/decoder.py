from modules.parser.decoder.header_decoder import HeaderDecoder
from modules.parser.decoder.payload_decoder import PayloadDecoder


class Decoder:
    raw = None
    response = {}

    def __init__(self, data):
        self.raw = data

    def header(self):
        self.response["header"] = HeaderDecoder(self.raw).decode().get_model()

    def payload(self):
        self.response["payload"] = (
            PayloadDecoder(self.response["header"]["protocol_id"], self.raw)
            .decode()
            .get_result()
        )

        print("Device id: ", self.response["header"]["device_id"].decode())

        self.response["payload"]["device_id"] = (
            self.response["header"]["device_id"].decode().rstrip("\x00")
        )

    def execute(self):
        self.header()
        self.payload()

        return self

    def get_result(self):
        return self.response
