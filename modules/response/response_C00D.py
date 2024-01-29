class MainC00DResponse:
    def __init__(self, data):
        self.data = data

    def make(self):
        return self.data["payload"]["ic_data"]
