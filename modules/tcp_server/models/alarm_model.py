class Alarm_Model:

    class Alarm_Data:
        new_alarm_flag = None
        alarm_type = None
        alarm_description = None
        alarm_threshold = None


    def __init__(self):
        self.alarm_count = 0
        self.alarm_data = []

    def set(self, param, value):
        setattr(self, param, value)

    def new_alarm_data(self):
        return self.Alarm_Data()

    def add_alarm_data(self, item):
        self.alarm_data.append(item)