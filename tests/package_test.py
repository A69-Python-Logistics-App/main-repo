import unittest
from models.Package import Package
from models.Customer import Customer

# CUSTOMER
VALID_NAME = "EMKO"
VALID_EMAIL = "emko@abv.bg"
VALID_CUSTOMER = Customer(VALID_NAME, VALID_EMAIL)
INVALID_NAME = "E"
INVALID_EMAIL = "E@"

# PACKAGE
VALID_WEIGHT = 100
VALID_PICKUP = "RUSE"
VALID_DROPOFF = "VARNA"
INVALID_WEIGHT = -100

class Package_Should(unittest.TestCase):

    def test_initializer_sets_properties_whenValidParams(self):
        # ARRANGE + ACT
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        # ASSERT
        self.assertEqual(VALID_WEIGHT, package._weight)
        self.assertEqual(VALID_PICKUP, package._pickup_loc)
        self.assertEqual(VALID_DROPOFF, package._dropoff_loc)
        self.assertEqual(VALID_CUSTOMER, package._contact)

    def test_initalizer_raises_ValueError_whenInvalidWeight(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Package(INVALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        