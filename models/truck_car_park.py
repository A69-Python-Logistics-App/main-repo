class TruckCarPark:
    def __init__(self):
        self.trucks = []
        self.initialize_trucks()

    def initialize_trucks(self):
        # Scania trucks
        for truck_id in range(1001, 1011):
            self.add_truck(Truck(truck_id, 42000))

        # Man trucks
        for truck_id in range(1011, 1026):
            self.add_truck(Truck(truck_id, 37000))

        # Actros trucks
        for truck_id in range(1026, 1041):
            self.add_truck(Truck(truck_id, 26000))

    def add_truck(self, truck):
        self.trucks.append(truck)

    def list_all_free_trucks(self):
        return [truck for truck in self.trucks if truck.is_free()]

class Truck:
    def __init__(self, truck_id, capacity):
        self.truck_id = truck_id
        self.capacity = capacity
        self.assigned_route = None

    def is_free(self):
        return self.assigned_route is None