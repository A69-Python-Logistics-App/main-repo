import unittest
from models.package import Package
from models.customer import Customer

# CUSTOMER
VALID_NAME = "EMKO"
VALID_EMAIL = "emko@abv.bg"
VALID_CUSTOMER = Customer(VALID_NAME, VALID_EMAIL)

# PACKAGE
VALID_WEIGHT = 100
VALID_PICKUP = "RUSE"
VALID_DROPOFF = "VARNA"

INVALID_WEIGHT = -100

class Package_Should(unittest.TestCase):

    def test_initializer_sets_properties_when_ValidParams(self):
        # ARRANGE
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER.id)
        # ACT
        VALID_CUSTOMER.add_package(package)
        # ASSERT
        self.assertEqual(VALID_WEIGHT, package._weight)
        self.assertEqual(VALID_PICKUP, package._pickup_loc)
        self.assertEqual(VALID_DROPOFF, package._dropoff_loc)
        self.assertEqual(VALID_CUSTOMER.id, package.id)

    def test_initializer_raises_ValueError_when_WeightBelowZero(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Package(INVALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER.id)

    def test_initializer_raises_ValueError_when_idIsInvalid(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)

    def test_advancePackageStatus_advancesStatus(self):
        # ARRANGE
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER.id)
        # ACT
        previous_status = package.status
        package.advance_package_status()
        status = package.status
        # ASSERT
        self.assertNotEqual(previous_status, status)