

class Truck:
    def __init__(self,truck_name:str, truck_id:int, truck_capacity:int, truck_range:int):
        self.name = truck_name
        self.id = truck_id
        self.capacity = truck_capacity
        self.range = truck_range
        self._assigned_route = False

    @property
    def is_assigned(self):
        return self._assigned_route
    
    @is_assigned.setter
    def is_assigned(self, bool:bool):
        self._assigned_route = bool
        print(self._assigned_route)

    def is_free(self):
        return not self._assigned_route