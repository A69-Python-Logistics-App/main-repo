
from models.truck import Truck
from models.Package import Package
class Location:
    Cities = ["Sydney", "Melbourne", "Adelaide", "Alice Springs", "Brisbane", "Darwin", "Perth"]

    def __init__(self,hub_name):
        if hub_name not in Location.Cities:
            raise ValueError("Invalid Location")
        self.hub_name = hub_name
        self.list_of_trucks_on_location:list[Truck] = []
        self.list_of_packages_on_location:list[Package] = []