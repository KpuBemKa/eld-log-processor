class Protocol4001Model:
    flag: int

    def set(self, param, value):
        setattr(self, param, value)
