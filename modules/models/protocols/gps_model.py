class GPS_Model:
    class GPS_Data:
        date: dict[str, int]
        time: dict[str, int]
        latitude: float
        longitude: float
        speed: float  # mph
        direction: int  # milli-degrees
        flag: dict[str, str]

    def __init__(self):
        self.gps_count = 0
        self.gps_data = []

    def set(self, param, value):
        setattr(self, param, value)

    def new_gps_data(self):
        return self.GPS_Data()

    def add_gps_data(self, item):
        self.gps_data.append(item)
