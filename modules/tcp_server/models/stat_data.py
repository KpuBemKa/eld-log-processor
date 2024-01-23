class StatData:
    last_accon_time = False
    UTC_Time = False
    total_trip_mileage = False
    current_trip_mileage = False
    total_fuel = False
    current_fuel = False
    vstate = {}
    reserved = False

    def set(self, param, value):
        setattr(self, param, value)
