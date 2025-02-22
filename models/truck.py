

class Truck:
    def __init__(self,truck_name:str, truck_id:int, truck_capacity:int, truck_range:int):
        self.name = truck_name
        self.id = truck_id
        self.capacity = truck_capacity
        self.range = truck_range
        self._is_free = True

    @property
    def is_free(self):
        return self._is_free
    
    @is_free.setter
    def is_free(self, bool:bool):
        self._is_free = bool

