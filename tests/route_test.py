import unittest
from models.route import Route
from datetime import datetime
from models.package import Package
from models.customer import Customer

class Route_Should(unittest.TestCase):
    VALID_CUSTOMER = Customer("customer", "customer@")
    VALID_PACKAGE = Package(5000, "SYD", "MEL", VALID_CUSTOMER.id)
    VALID_PACKAGE = Package(5000, "SYD", "MEL", VALID_CUSTOMER.id)
    VALID_ROUTE = Route(stops=["SYD", "MEL"], departure_time=datetime.now())
    VALID_ROUTE_2 = Route(stops=["SYD", "MEL"], departure_time=datetime.now())


    def test_route_raises_error_when_stops_less_than_two(self):
        with self.assertRaises(ValueError):
            route = Route(stops=["SYD"], departure_time=datetime.now())
    
    def test_add_package_weight_correctly(self):
        route = self.VALID_ROUTE
        route.assign_truck(1002, 20_000)
        route.add_package(self.VALID_PACKAGE)
        
        self.assertEqual(route.current_weight, 5000)
    
    def test_add_package_raises_error_when_capacity_exceeded(self):
        package = self.VALID_PACKAGE
        route = self.VALID_ROUTE_2
        route.assign_truck(1003, 40_000)
        route.add_package(package)
        package_2 = Package(40_000,"SYD","MEL", self.VALID_CUSTOMER.id)
        package_2 = Package(40_000,"SYD","MEL", self.VALID_CUSTOMER.id)

        with self.assertRaises(ValueError):
            route.add_package(package_2)
    
    def test_route_prints_correctly_info_about_the_route(self):
        pass


