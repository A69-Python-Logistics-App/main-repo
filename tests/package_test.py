import unittest
from datetime import datetime
from models.package import Package

class TestPackage(unittest.TestCase):

    def setUp(self):
        self.weight = 10
        self.pickup_loc = "Location A"
        self.dropoff_loc = "Location B"
        self.customer_id = 123
        self.date_creation = datetime.now()

    def test_package_initialization(self):
        package = Package(self.weight, self.pickup_loc, self.dropoff_loc, self.customer_id, self.date_creation)
        self.assertEqual(package.weight, self.weight)
        self.assertEqual(package.pickup_location, self.pickup_loc)
        self.assertEqual(package.dropoff_location, self.dropoff_loc)
        self.assertEqual(package.current_location, self.pickup_loc)
        self.assertEqual(package.customer_id, self.customer_id)
        self.assertEqual(package.date_creation, self.date_creation)
        self.assertEqual(package.status, "Collected")
        self.assertEqual(package.id, 1002)

    def test_package_id_increment(self):
        package1 = Package(self.weight, self.pickup_loc, self.dropoff_loc, self.customer_id, self.date_creation)
        package2 = Package(self.weight, self.pickup_loc, self.dropoff_loc, self.customer_id, self.date_creation)
        self.assertEqual(package1.id, 1000)
        self.assertEqual(package2.id, 1001)

    def test_negative_weight_raises_value_error(self):
        with self.assertRaises(ValueError):
            Package(-1, self.pickup_loc, self.dropoff_loc, self.customer_id, self.date_creation)