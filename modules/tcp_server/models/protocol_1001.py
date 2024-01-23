class Protocol1001Model:
    software_version = None
    hardware_version = None
    new_parameter_count = None

    def set(self, param, value):
        setattr(self, param, value)
