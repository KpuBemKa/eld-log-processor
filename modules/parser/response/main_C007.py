


class MainC007Response:
    response = {}

    def __init__(self, data):
        self.data = data

    def make(self):
        return self.data['payload']['alarm_seq']
