from .decoder import Decoder
from ..response.response import Response
from modules.processing.processing import Processing


class Protocol:
    data = None

    def __init__(self, connection):
        self.connection = connection
        self.orig = None

    def decode(self, data):
        self.orig = data
        self.data = Decoder(data).execute().get_result()
        print("Decoded: ", self.data)
        return self

    def processing(self):
        Processing().process(self.data)
        return self

    def encode(self):
        response = Response(self.connection, self.data).make()
        # print('res', self.data, response)
        return response

    def additional(self):
        if Processing().additional_check(self.data) is False:
            Response(self.connection, self.data).make()

    def set_data(self, data):
        self.data = data