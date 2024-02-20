class Protocol400BModel:
    fault_flag: dict[int, str] = {}
    fault_count: int = 0
    fault_type_array = []
    mil_status = None

    class DTC_Model:
        code = None
        attr = None
        occurence = None

    def set(self, param, value):
        setattr(self, param, value)

    def getDTC_Model(self):
        return self.DTC_Model()

    def add_fault(self, item):
        self.fault_type_array.append(item)
        return self
