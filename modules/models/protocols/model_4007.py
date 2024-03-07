class Protocol4007Model:
    alarm_seq: int
    alarm_count: int
    alarm_array: list

    def set(self, param, value):
        setattr(self, param, value)
