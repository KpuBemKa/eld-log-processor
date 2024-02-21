class StatData:
    last_accon_time: int
    utc_time: int
    total_trip_mileage: int
    current_trip_mileage: int
    total_fuel: int
    current_fuel: int
    vstate: dict[str, bool]
    reserved: dict[str, str]

    def set(self, param, value):
        setattr(self, param, value)
