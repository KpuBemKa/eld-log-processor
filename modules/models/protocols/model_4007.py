class Protocol4007Model:
    alarm_seq = None
    alarm_count = None
    alarm_array = None

    def set(self, param, value):
        setattr(self, param, value)
