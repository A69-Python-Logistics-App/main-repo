
class Truck:
    def __init__(self,truck_name:str, truck_id:int, truck_capacity:int, truck_range:int):
        self._name = truck_name
        self._id = truck_id
        self._capacity = truck_capacity
        self._range = truck_range
        self._current_location = "Car Park"
        self._is_free = True

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def range(self):
        return self._range
    
    @property
    def current_location(self):
        return self._current_location
    
    @current_location.setter
    def current_location(self, location:str):
        if type(location) != str:
            raise ValueError("current_location accepts string only")
        self._current_location = location

    @property
    def is_free(self):
        return self._is_free
    
    @is_free.setter
    def is_free(self, value:bool):
        if type(value) != bool:
            raise ValueError("is_free accepts bool only")
        self._is_free = value

    def __str__(self):
        return f"#{self.id} {self.name.center(6, " ")} : capacity: {self.capacity}kg, range: {self.range}km | Free: {self.is_free} | Location in {self.current_location}"

