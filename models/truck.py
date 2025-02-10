


class Truck:
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

    last_ids = {
        SCANIA: SCANIA_ID,
        MAN: MAN_ID,
        ACTROS: ACTROS_ID
    }


    def __init__(self,name):
        valid_trucks = [Truck.SCANIA, Truck.MAN, Truck.ACTROS]
        if name not in valid_trucks:
            raise ValueError(f"Invalid truck name: {name}")
        self.name = name
        if name == Truck.SCANIA:
            self.capacity = Truck.CAP_SCANIA
            self.max_range = Truck.SCANIA_MAX_RANGE
        elif name == Truck.MAN:
            self.capacity = Truck.CAP_MAN
            self.max_range = Truck.MAN_MAX_RANGE
        elif name == Truck.ACTROS:
            self.capacity = Truck.CAP_ACTROS
            self.max_range = Truck.ACTROS_MAX_RANGE
        
        self.current_range = self.max_range
        self.truck_id = Truck.last_ids[name]
        Truck.last_ids[name] += 1
        
    def __str__(self):
        return f"Truck {self.name} ID{self.truck_id}"
