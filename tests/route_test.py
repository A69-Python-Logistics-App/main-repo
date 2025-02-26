import unittest
from models.route import Route
from datetime import datetime,timedelta
from models.package import Package
from models.truck import Truck

class Route_Should(unittest.TestCase):

    def test_route_correct_initialization(self):
        departure_time = datetime.now()
        route = Route(stops=["SYD", "MEL"], departure_time = departure_time)
        
        self.assertEqual(route.stops, ["SYD", "MEL"])
        self.assertTrue(abs((route.route_stop_estimated_arrival[0] - departure_time).total_seconds())<1)
    
    def test_raises_value_error_when_invalid_stops(self):
        departure_time = datetime.now()
        invalid_stops = ["a","b"]
    
        with self.assertRaises(ValueError):
            route = Route(stops=invalid_stops, departure_time=departure_time)
    
    def test_calculates_distances_correctly(self):
        departure_time = datetime.now()
        route = Route(stops=["SYD", "MEL"], departure_time = departure_time)
        distance_SYD_MEL = 877

        self.assertEqual(route.route_total_distance, distance_SYD_MEL)
    
    def test_deliver_packages_correctly(self):
        package_1 = Package(100,"SYD","MEL",1,date_creation=datetime.now())
        package_2 = Package(200,"SYD","BRI",1,date_creation=datetime.now())
        departure_time = datetime.now()
        route = Route(stops=["SYD", "MEL"], departure_time = departure_time)

        route.list_of_packages = [package_1, package_2]
        route.current_weight = 300
        delivered = route.deliver_packages("MEL")

        self.assertEqual(len(delivered), 1)
        self.assertEqual(delivered[0].status, "Delivered")
        self.assertEqual(delivered[0].current_location, "MEL")
        self.assertEqual(route.current_weight, 200)
        self.assertNotIn(package_1, route.list_of_packages)
    
    def test_add_package_correctly(self):
        package_1 = Package(100,"SYD","MEL",1,date_creation=datetime.now())
        departure_time = datetime.now()
        route = Route(stops=["SYD", "MEL"], departure_time = departure_time)
        truck = Truck("TestTruck", 1, 40_000, 8000)
        route.assign_truck(truck)
        route.add_package(package_1)

        self.assertEqual(route.current_weight, 100)
        self.assertIn(package_1, route.list_of_packages)

    def test_add_package_raises_value_error_when_capacity_exceeded(self):  
        package_1 = Package(50_000,"SYD","MEL",1,date_creation=datetime.now())
        departure_time = datetime.now()
        route = Route(stops=["SYD", "MEL"], departure_time = departure_time)
        truck = Truck("TestTruck", 1, 40_000, 8000)
        route.assign_truck(truck)

        with self.assertRaises(ValueError):
            route.add_package(package_1)
        
    def test_unassign_truck_correctly(self):
        package_1 = Package(20_000,"SYD","MEL",1,date_creation=datetime.now())
        departure_time = datetime.now()
        route = Route(stops=["SYD", "MEL"], departure_time = departure_time)
        truck_1 = Truck("TestTruck", 1, 40_000, 8000)
        route.assign_truck(truck_1)
        route.unassign_truck(truck_1)
        expected_number_of_trucks = 0
        self.assertEqual(len(route.assigned_trucks), expected_number_of_trucks)
    
    def test_unassign_all_trucks_correctly(self):
        departure_time = datetime.now()
        route = Route(stops=["SYD", "MEL"], departure_time = departure_time)
        truck_1 = Truck("TestTruck", 1, 40_000, 8000)
        truck_2 = Truck("TestTruck2", 2, 40_000, 8000)
        route.assign_truck(truck_1)
        route.assign_truck(truck_2)
        expected_number_of_trucks = 0
        route.unassign_all_trucks()
        self.assertEqual(len(route.assigned_trucks), expected_number_of_trucks)


    



