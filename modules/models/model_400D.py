class Protocol400DModel:
    stat_data = None
    gps_data = None
    ic_data = None

    def set(self, param, value):
        setattr(self, param, value)
