class EventsProcessing:
    data = None

    def __init__(self, data):
        self.data = data

    def process(self):
        match (self.data["header"]["protocol_id"]):
            case "1001":
                print("Found login packet")
