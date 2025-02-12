

from models.truck_type import TruckType


class TruckCarPark:
    SCANIA = "Scania"
    MAN = "MAN"
    ACTROS = "ACTROS"

    CAP_SCANIA = 42_000
    CAP_MAN = 37_000
    CAP_ACTROS = 26_000
    
    SCANIA_ID = 1001
    MAN_ID = 1011
    ACTROS_ID = 1026

    SCANIA_MAX_RANGE = 8000
    MAN_MAX_RANGE = 10_000
    ACTROS_MAX_RANGE = 26_000

    SCANIA_TRUCK_COUNT = 10
    MAN_TRUCK_COUNT = 15
    ACTROS_TRUCK_COUNT = 15

    def __init__(self):
        self.truck_types: list[TruckType] = [
            TruckType(self.SCANIA, self.CAP_SCANIA, self.SCANIA_MAX_RANGE, self.SCANIA_ID, self.SCANIA_TRUCK_COUNT),
            TruckType(self.MAN, self.CAP_MAN, self.MAN_MAX_RANGE, self.MAN_ID, self.MAN_TRUCK_COUNT),
            TruckType(self.ACTROS, self.CAP_ACTROS, self.ACTROS_MAX_RANGE, self.ACTROS_ID, self.ACTROS_TRUCK_COUNT)
        ]

    def list_all_free_trucks():
        # for truck_type in truck_types:
            # print_truck_type_free_info()
        pass