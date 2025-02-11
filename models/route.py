from datetime import datetime, timedelta
from models.Package import Package

class Route:
    route_counter = 1

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
    
    def __init__(self, stops:list, departure_time: datetime):
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

        current_stop_estimated_time_of_arrival = departure_time
        for i in range(len(stops) -1):
            current_stop = stops[i]
            next_stop = stops[i + 1]
            distance_to_next_stop = self.distances[current_stop][next_stop]

            self.route_total_distance += distance_to_next_stop

            hours_to_next_stop = timedelta(hours=(distance_to_next_stop / self.AVG_TRUCK_SPEED))
            next_stop_estimated_time_of_arrival = current_stop_estimated_time_of_arrival + hours_to_next_stop
            self.route_stop_estimated_arrival.append(next_stop_estimated_time_of_arrival)

            current_stop_estimated_time_of_arrival = next_stop_estimated_time_of_arrival
    
    def __str__(self):
        route_info = f"This route has {len(self.stops)} stops:\n"
        route_info += f"Departure time is: {self.route_stop_estimated_arrival[0]}\n"
        route_info += f"Total distance is: {self.route_total_distance} km\n"

        return route_info
    
    def assign_truck(self, truck_id: int, truck_capacity: int):
        if truck_capacity < self.current_weight:
            raise ValueError(f"Truck has {truck_capacity}kg capacity but {self.current_weight}kg is needed")
        self.truck_id = truck_id
        self.weight_capacity = truck_capacity


    def add_package(self, package):
        if self.current_weight + package.weight > self.weight_capacity:
            raise ValueError(f"Package weight exceeds the capacity. Capacity is {self.weight_capacity - self.current_weight}")
        self.current_weight += package.weight