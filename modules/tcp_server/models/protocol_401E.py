class Protocol401EModel:
    error_code =None

    def set(self, param, value):
        setattr(self, param, value)

    def getDTC_Model(self):
        return self.DTC_Model()

    def add_fault(self, item):
        self.fault_type_array.append(item)
        return self