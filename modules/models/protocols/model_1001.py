class Protocol1001Model:
    software_version: str
    hardware_version: str
    new_parameter_count: int
    new_parameters: list[int] = []

    def set(self, param, value):
        setattr(self, param, value)
