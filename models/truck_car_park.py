from models.truck import Truck

class TruckCarPark:

    SCANIA = "SCANIA"
    MAN = "MAN"
    ACTROS = "ACTROS"

    CAP_SCANIA = 42000
    CAP_MAN = 37000
    CAP_ACTROS = 26000

    SCANIA_MAX_RANGE = 8000
    MAN_MAX_RANGE = 10000
    ACTROS_MAX_RANGE = 26000

    def __init__(self):
        
        self.trucks:list[Truck] = []
        self.initialize_trucks()

    def initialize_trucks(self):
        # Scania trucks
        for truck_id in range(1001, 1011):
            self.add_truck(Truck(self.SCANIA, truck_id, self.CAP_SCANIA, self.SCANIA_MAX_RANGE))

        # Man trucks
        for truck_id in range(1011, 1026):
            self.add_truck(Truck(self.MAN, truck_id, self.CAP_MAN, self.MAN_MAX_RANGE))

        # Actros trucks
        for truck_id in range(1026, 1041):
            self.add_truck(Truck(self.ACTROS, truck_id, self.CAP_ACTROS, self.ACTROS_MAX_RANGE))

    def add_truck(self, truck):
        self.trucks.append(truck)

    def list_all_free_trucks(self):
        return [truck for truck in self.trucks if truck.is_free]
    
    def find_free_truck_by_name(self, name:str):
        free_trucks = self.list_all_free_trucks()
        for truck in free_trucks:
            if truck.name == name:
                return truck
        raise ValueError(f"No trucks with name '{name}' are available")
    
    def find_truck_by_id(self, id:int):
        for truck in self.trucks:
            if truck.id == id:
                return truck
        raise ValueError(f"No truck with '{id}' found")

