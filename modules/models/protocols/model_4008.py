class Protocol4008Model:
    local_area_code = None
    cell_id = None

    def set(self, param, value):
        setattr(self, param, value)
