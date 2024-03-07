class Protocol4008Model:
    local_area_code: int
    cell_id: int

    def set(self, param, value):
        setattr(self, param, value)
