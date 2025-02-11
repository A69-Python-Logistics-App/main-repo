import unittest
from models.route import Route
from datetime import datetime, timedelta
from models.Package import Package
from models.Customer import Customer

class TestRout_Should(unittest.TestCase):
    VALID_CUSTOMER = Customer("customer", "customer@")
    VALID_PACKAGE = Package(5000, "SYD", "MEL", VALID_CUSTOMER)
    VALID_ROUTE = Route(stops=["SYD", "MEL"], departure_time=datetime.now())


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
        route = self.VALID_ROUTE
        route.assign_truck(1002, 40_000)
        route.add_package(package)
        package_2 = Package(40_000,"SYD","MEL", self.VALID_CUSTOMER)

        with self.assertRaises(ValueError):
            route.add_package(package_2)


