import unittest
from models.Package import Package
from models.Customer import Customer

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
        # ARRANGE + ACT
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        # ASSERT
        self.assertEqual(VALID_WEIGHT, package._weight)
        self.assertEqual(VALID_PICKUP, package._pickup_loc)
        self.assertEqual(VALID_DROPOFF, package._dropoff_loc)
        self.assertEqual(VALID_CUSTOMER, package._customer)

    def test_initializer_raises_ValueError_when_WeightBelowZero(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Package(INVALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)

    def test_initializer_increments_id_when_ValidParams(self):
        # ARRANGE + ACT
        package_1 = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        package_2 = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        # ASSERT
        self.assertGreater(package_2.id, package_1.id)

    def test_advancePackageStatus_advancesStatus(self):
        # ARRANGE
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        # ACT
        previous_status = package.status
        package.advance_package_status()
        status = package.status
        # ASSERT
        self.assertNotEqual(previous_status, status)

    def test_findPackageById_raises_ValueError_when_idNotFound(self):
        # ARRANGE
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        # ACT + ASSERT
        with self.assertRaises(ValueError):
            _ = package.find_package_by_id(100)

    # VALID_PACKAGE_INFO formatting is up to debate. 
    # If it's different, you can probably ignore this test.
    def test_findPackageById_returns_valid_packageInfo(self):
        # ARRANGE
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        VALID_PACKAGE_INFO = "\n".join([
        f"## Customer info: {VALID_NAME}, {VALID_EMAIL}",
        f"#  Package id: {package.id}, Status: {package.status}",
        f"#  Package date creation: {package._date_creation}",
        f"#  Package pickup location: {package._pickup_loc}",
        f"#  Package current location: {package._current_loc}",
        f"#  Package destination: {package._dropoff_loc}",
        f"#  Package weight: {package.weight} KG"
        ])
        # ACT
        info = package.find_package_by_id(3)
         # id is 3, because 3 packages have been added. TODO: Find out how Mock works,
         # so a new instance of Class Package() can be made for every test.

        # ASSERT
        self.assertEqual(VALID_PACKAGE_INFO, info)

    # VALID_PACKAGE_INFO formatting is up to debate. 
    # If it's different, you can probably ignore this test.
    def test_packageInfo_returns_correctlyFormatted(self):
        # ARRANGE
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        VALID_PACKAGE_INFO = "\n".join([
        f"## Customer info: {VALID_NAME}, {VALID_EMAIL}",
        f"#  Package id: {package.id}, Status: {package.status}",
        f"#  Package date creation: {package._date_creation}",
        f"#  Package pickup location: {package._pickup_loc}",
        f"#  Package current location: {package._current_loc}",
        f"#  Package destination: {package._dropoff_loc}",
        f"#  Package weight: {package.weight} KG"
        ])
        # ACT
        info = package.package_info()
        # ASSERT
        self.assertEqual(VALID_PACKAGE_INFO, info)

    # REALTIME_INFO IS UP TO DEBATE. CHECK DOCSTRING.
    def test_realTimeInfo_returns_correctlyFormatted(self):
        # ARRANGE
        package = Package(VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_CUSTOMER)
        VALID_REALTIME_INFO = "\n".join([
            f"# Package current location: {package._current_loc}",
            f"# Package creation date: {package._date_creation}"
        ])
        # ACT
        info = package.realtime_info()
        # ASSERT
        self.assertEqual(VALID_REALTIME_INFO, info)
        
    