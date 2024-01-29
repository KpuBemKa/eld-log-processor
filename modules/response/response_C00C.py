class MainC00CResponse:
    def __init__(self, data):
        self.data = data

    def make(self):
        return self.data["payload"]["card_id"]
