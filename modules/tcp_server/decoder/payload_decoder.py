from .decoder import Decoder
from modules.tcp_server.decoder.payload.protocol_1001 import Protocol1001Decoder
from modules.tcp_server.decoder.payload.protocol_4001 import Protocol4001Decoder
from modules.tcp_server.decoder.payload.protocol_4007 import Protocol4007Decoder
from modules.tcp_server.decoder.payload.protocol_400B import Protocol400BDecoder
from modules.tcp_server.decoder.payload.protocol_4008 import Protocol4008Decoder
from modules.tcp_server.decoder.payload.protocol_4009 import Protocol4009Decoder


class PayloadDecoder(Decoder):
    def __init__(self, protocol, data):
        self.protocol = protocol
        self.data = data[27:-4]
        self.result = {}

    def decode(self):
        print("protocol", self.protocol)

        match self.protocol:
            case "1001":
                self.protocol_1001()

            case "1002":
                self.exit()

            case "1003":
                pass

            case "4007":
                self.protocol_4007()

            case "a002":
                pass

            case "4001":
                self.protocol_4001()

            case "400B":
                self.protocol_400B()

            case "4002":
                pass

            case "4008":
                self.protocol_4008()

            case "4009":
                self.protocol_4009()

            case "4011":
                self.protocol_4001()

            case "401E":
                self.protocol_401e()

            case "401F":
                pass

            case "4020":
                pass

            case _:
                pass

        return self

    def protocol_1001(self):
        self.result = Protocol1001Decoder(self.data).decode().get_result()

    def protocol_4001(self):
        self.result = Protocol4001Decoder(self.data).decode().get_result()

    def protocol_4007(self):
        self.result = Protocol4007Decoder(self.data).decode().get_result()

    def protocol_400B(self):
        self.result = Protocol400BDecoder(self.data).decode().get_result()

    def protocol_4008(self):
        self.result = Protocol4008Decoder(self.data).decode().get_result()

    def protocol_4009(self):
        self.result = Protocol4009Decoder(self.data).decode().get_result()

    def protocol_a002(self):
        # self.result =
        pass

    def protocol_401e(self):
        # self.result =
        pass

    def exit(self):
        exit()

    def get_result(self):
        return self.result
