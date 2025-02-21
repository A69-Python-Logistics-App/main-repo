class Truck:
    def __init__(self,truck_name:str, truck_id:int, truck_capacity:int, truck_range:int):
        self.name = truck_name
        self.id = truck_id
        self.capacity = truck_capacity
        self.range = truck_range
        self.assigned_route = None

    def is_free(self):
        return self.assigned_route is None