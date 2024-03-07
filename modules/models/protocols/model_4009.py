class Protocol4009Model:
    utc_time: int
    gps_item: dict

    def set(self, param, value):
        setattr(self, param, value)
