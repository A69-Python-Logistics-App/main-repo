from models.helpers.validation_helpers import parse_to_int
from datetime import datetime, timedelta
from models.location import Location
from models.package import Package
from models.truck import Truck


class Route:

    __ID = 1

    __AVG_TRUCK_SPEED = 87

    __SYDNEY_CODE = "SYD"
    __MELBOURNE_CODE = "MEL"
    __ADELAIDE_CODE = "ADL"
    __ALICE_SPRINGS_CODE = "ASP"
    __BRISBANE_CODE = "BRI"
    __DARWIN_CODE = "DAR"
    __PERTH_CODE = "PER"

    __DISTANCES = {
        __SYDNEY_CODE:{__SYDNEY_CODE:0, __MELBOURNE_CODE :877, __ADELAIDE_CODE:1376,__ALICE_SPRINGS_CODE:2762, __BRISBANE_CODE:909, __DARWIN_CODE:3935, __PERTH_CODE:4016},
        __MELBOURNE_CODE:{__SYDNEY_CODE: 877, __MELBOURNE_CODE :0, __ADELAIDE_CODE:725, __ALICE_SPRINGS_CODE:725, __BRISBANE_CODE:1765,__DARWIN_CODE:3752,__PERTH_CODE:3509},
        __ADELAIDE_CODE:{__SYDNEY_CODE: 1376, __MELBOURNE_CODE :725, __ADELAIDE_CODE:0, __ALICE_SPRINGS_CODE:1530, __BRISBANE_CODE:1927,__DARWIN_CODE:3027,__PERTH_CODE:2785},
        __ALICE_SPRINGS_CODE:{__SYDNEY_CODE:2762, __MELBOURNE_CODE :2255, __ADELAIDE_CODE:1530, __ALICE_SPRINGS_CODE:0, __BRISBANE_CODE:1927,__DARWIN_CODE:3027,__PERTH_CODE:2785},
        __BRISBANE_CODE:{__SYDNEY_CODE:909, __MELBOURNE_CODE:1765, __ADELAIDE_CODE:1927, __ALICE_SPRINGS_CODE:2993, __BRISBANE_CODE:0,__DARWIN_CODE:3462,__PERTH_CODE:4311},
        __DARWIN_CODE:{__SYDNEY_CODE:3935, __MELBOURNE_CODE:3752, __ADELAIDE_CODE:3027, __ALICE_SPRINGS_CODE:1497, __BRISBANE_CODE:3426,__DARWIN_CODE:0,__PERTH_CODE:4025},
        __PERTH_CODE:{__SYDNEY_CODE:4016, __MELBOURNE_CODE:3509, __ADELAIDE_CODE:2785, __ALICE_SPRINGS_CODE:2481, __BRISBANE_CODE:4311,__DARWIN_CODE:4025,__PERTH_CODE:0},    
    }
    
    def __init__(self, stops: tuple, departure_time: datetime):
        Location.validate_locations(stops)
        if len(stops) < 2:
            raise ValueError("Route needs to be at least 2 stops")
        
        self.id = Route.__ID
        Route.__ID += 1

        self.stops = stops
        self.route_total_distance = 0
        self.route_stop_estimated_arrival = [departure_time]

        self._assigned_trucks:list[Truck] = []
        self.weight_capacity = 0
        self.current_weight = 0

        self.route_total_distance, self.route_stop_estimated_arrival = self.calculate_route_timeline(departure_time, stops)
        self.list_of_packages:list[Package] = []
    
    def __str__(self):
        result = f"Route ID: {self.id}\n"
        result += f"Stops {' -> '.join(self.stops)}\n"
        result += f"Total distance: {self.route_total_distance}km\n"
        result += f"Estimated arrivals:\n"
        for i in range(len(self.stops)):
            result += f" - {self.stops[i]}: {self.route_stop_estimated_arrival[i].strftime('%Y-%m-%d %H:%M')}\n"

        result = result[:-1]
        if len(self._assigned_trucks) > 0:
            for truck in self._assigned_trucks:
                result += f"\n Assigned Truck '{truck.name}' ID:{truck.id}, currently in {truck.current_location}"

            result += f"\n Remaining capacity: {self.weight_capacity - self.current_weight} kg" 
        else:
            result += f"\n No trucks assigned"

        return result
    
    @classmethod
    def set_internal_id(self, ID:int):
        """
        Set class __ID to the given value.
        """
        Package.__ID = parse_to_int(ID)

    @property
    def assigned_trucks(self):
        return tuple(self._assigned_trucks)

    def _recalculate_capacity(self):
        """
        Calculate route capacity based on truck capacities.
        """
        self.weight_capacity = 0
        for truck in self._assigned_trucks:
            self.weight_capacity += truck.capacity

    def calculate_route_timeline(self,departure_time, stops:list[str]):
        route_total_distance = 0
        route_stop_estimated_arrival = [departure_time]
        current_stop_estimated_time_of_arrival = departure_time

        for i in range(len(stops) -1):
            current_stop = stops[i]
            next_stop = stops[i + 1]
            distance_to_next_stop = self.__DISTANCES[current_stop][next_stop]

            route_total_distance += distance_to_next_stop

            hours_to_next_stop = timedelta(hours=(distance_to_next_stop / self.__AVG_TRUCK_SPEED))
            next_stop_estimated_time_of_arrival = current_stop_estimated_time_of_arrival + hours_to_next_stop
            route_stop_estimated_arrival.append(next_stop_estimated_time_of_arrival)

            current_stop_estimated_time_of_arrival = next_stop_estimated_time_of_arrival
        
        return route_total_distance,route_stop_estimated_arrival

    def add_package(self, package:Package):
        """
        This method adds a package to the current weight and updates it.
        :params: package(Package) the package to be added
        Raises ValueError if the total weight exceeds the weight capacity
        """
        if self.current_weight + package.weight > self.weight_capacity:
            raise ValueError(f"Package weight exceeds the capacity. Capacity is {self.weight_capacity - self.current_weight}")
        self.current_weight += package.weight
    
    def deliver_packages(self, stop: str):
        """
        Method to deliver packages.
        """
        delivered_packages = []
        for package in self.list_of_packages[:]:
            if package.dropoff_location == stop:
                package.update_status("Delivered")
                package.update_location(stop)
                delivered_packages.append(package)
                self.list_of_packages.remove(package)
                self.current_weight -= package.weight
                self._recalculate_capacity()
        return delivered_packages
    
    def assign_truck(self, truck:Truck):
        """
        Assignes a truck to route.
        """
        if type(truck) != Truck:
            raise ValueError("Assign truck accepts truck type only")
        truck.is_free = False
        truck.current_location = self.stops[0]
        self._assigned_trucks.append(truck)
        self._recalculate_capacity()

    def unassign_truck(self, truck:Truck):
        """
        Unassign a specific truck from route.
        """
        if type(truck) != Truck:
            raise ValueError("Unassign truck accepts truck type only")
        truck.reset()
        self._assigned_trucks.remove(truck)
        self._recalculate_capacity()
    
    def unassign_all_trucks(self):
        """
        Unassignes and resets all trucks from route.
        """
        [truck.reset() for truck in self._assigned_trucks]
        self._assigned_trucks.clear()
        self._recalculate_capacity()