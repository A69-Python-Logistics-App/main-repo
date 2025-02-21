from datetime import datetime, timedelta
from models.package import Package
from models.truck_carpark import TruckCarPark
from models.location import Location
from models.helpers.validation_helpers import parse_to_int

class Route:
    route_counter = 1
    list_of_all_routes = []

    AVG_TRUCK_SPEED = 87
    SYDNEY_CODE = "SYD"
    MELBOURNE_CODE = "MEL"
    ADELAIDE_CODE = "ADL"
    ALICE_SPRINGS_CODE = "ASP"
    BRISBANE_CODE = "BRI"
    DARWIN_CODE = "DAR"
    PERTH_CODE = "PER"

    distances = {
        SYDNEY_CODE:{SYDNEY_CODE:0, MELBOURNE_CODE :877, ADELAIDE_CODE:1376,ALICE_SPRINGS_CODE:2762, BRISBANE_CODE:909, DARWIN_CODE:3935, PERTH_CODE:4016},
        MELBOURNE_CODE:{SYDNEY_CODE: 877, MELBOURNE_CODE :0, ADELAIDE_CODE:725, ALICE_SPRINGS_CODE:725, BRISBANE_CODE:1765,DARWIN_CODE:3752,PERTH_CODE:3509},
        ADELAIDE_CODE:{SYDNEY_CODE: 1376, MELBOURNE_CODE :725, ADELAIDE_CODE:0, ALICE_SPRINGS_CODE:1530, BRISBANE_CODE:1927,DARWIN_CODE:3027,PERTH_CODE:2785},
        ALICE_SPRINGS_CODE:{SYDNEY_CODE:2762, MELBOURNE_CODE :2255, ADELAIDE_CODE:1530, ALICE_SPRINGS_CODE:0, BRISBANE_CODE:1927,DARWIN_CODE:3027,PERTH_CODE:2785},
        BRISBANE_CODE:{SYDNEY_CODE:909, MELBOURNE_CODE:1765, ADELAIDE_CODE:1927, ALICE_SPRINGS_CODE:2993, BRISBANE_CODE:0,DARWIN_CODE:3462,PERTH_CODE:4311},
        DARWIN_CODE:{SYDNEY_CODE:3935, MELBOURNE_CODE:3752, ADELAIDE_CODE:3027, ALICE_SPRINGS_CODE:1497, BRISBANE_CODE:3426,DARWIN_CODE:0,PERTH_CODE:4025},
        PERTH_CODE:{SYDNEY_CODE:4016, MELBOURNE_CODE:3509, ADELAIDE_CODE:2785, ALICE_SPRINGS_CODE:2481, BRISBANE_CODE:4311,DARWIN_CODE:4025,PERTH_CODE:0},    
    }
    
    def __init__(self, stops:list[str], departure_time: datetime):
        Location.validate_locations(stops)
        if len(stops) < 2:
            raise ValueError("Route needs to be at least 2 stops")
        self.route_id = Route.route_counter
        Route.route_counter += 1
        self.stops = stops
        self.route_total_distance = 0
        self.route_stop_estimated_arrival = [departure_time]
        self.truck_id = None
        self.weight_capacity = None
        self.current_weight = 0
        self.route_total_distance, self.route_stop_estimated_arrival = self.calculate_route_timeline(departure_time, stops)
        self.list_of_packages:list[Package] = []

        Route.list_of_all_routes.append(self)

        
    def calculate_route_timeline(self,departure_time, stops:list[str]):
        route_total_distance = 0
        route_stop_estimated_arrival = [departure_time]
        current_stop_estimated_time_of_arrival = departure_time

        for i in range(len(stops) -1):
            current_stop = stops[i]
            next_stop = stops[i + 1]
            distance_to_next_stop = self.distances[current_stop][next_stop]

            route_total_distance += distance_to_next_stop

            hours_to_next_stop = timedelta(hours=(distance_to_next_stop / self.AVG_TRUCK_SPEED))
            next_stop_estimated_time_of_arrival = current_stop_estimated_time_of_arrival + hours_to_next_stop
            route_stop_estimated_arrival.append(next_stop_estimated_time_of_arrival)

            current_stop_estimated_time_of_arrival = next_stop_estimated_time_of_arrival
        
        return route_total_distance,route_stop_estimated_arrival
    
    def __str__(self):
        route_id = self.route_id
        stops = self.stops
        total_distance = self.route_total_distance
        estimated_arrivals = self.route_stop_estimated_arrival
        truck = self.truck_id
        result = f"Route ID: {route_id}\n"
        result += f"Stops {" -> ".join(stops)}\n"
        result += f"Total distance: {total_distance}km\n"
        result += f"Estimated arrivals:\n"
        for i in range(len(stops)):
            result += f" - {stops[i]}: {estimated_arrivals[i].strftime('%Y-%m-%d %H:%M')}\n"

        result = result[:-1]
        if truck:
            result += f"\n Assign Truck with ID: {truck} and Capacity {self.weight_capacity}kg"
        else:
            result += f"\n No Truck assigned"

        return result
    
    @classmethod
    def set_internal_id(self, ID:int):
        """
        Set class __ID to the given value.
        """
        Package.__ID = parse_to_int(ID)

        
    def assign_truck(self, truck_id: int, truck_capacity: int):
        """
        This method assigns a truck to a route.
        :params: truck_id:int and truck_capacity:int
        :return: None. The truck is assigned to the route
        """
        if truck_id not in TruckCarPark.list_all_free_trucks():
            raise ValueError(f"Truck with ID:{truck_id} is not available")
        if truck_capacity < self.current_weight:
            raise ValueError(f"Truck has {truck_capacity}kg capacity but {self.current_weight}kg is needed")
        self.truck_id = truck_id
        self.weight_capacity = truck_capacity


    def add_package(self, package:Package):
        """
        This method adds a package to the current weight and updates it.
        :params: package(Package) the package to be added
        Raises ValueError if the total weight exceeds the weight capacity
        """
        if self.current_weight + package.weight > self.weight_capacity:
            raise ValueError(f"Package weight exceeds the capacity. Capacity is {self.weight_capacity - self.current_weight}")
        self.current_weight += package.weight
