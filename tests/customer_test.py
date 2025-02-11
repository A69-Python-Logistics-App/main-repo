import unittest
from models.customer import Customer
from tests.package_test import VALID_CUSTOMER

# CUSTOMER
VALID_NAME = "EMKO"
VALID_EMAIL = "emko@abv.bg"
VALID_ID = 1
INVALID_ID = -100
INVALID_NAME = "E"
INVALID_EMAIL = "E@BG"
INVALID_EMAIL_NO_AMP = "EMKOABV.BG"

# PACKAGE
VALID_WEIGHT = 100
VALID_PICKUP = "RUSE"
VALID_DROPOFF = "VARNA"

class Customer_Should(unittest.TestCase):

    def test_initializer_sets_properties_when_ValidParams(self):
        # ARRANGE + ACT
        customer = Customer(VALID_NAME,VALID_EMAIL)
        # ASSERT
        self.assertEqual(VALID_NAME, customer.name)
        self.assertEqual(VALID_EMAIL, customer.email)

    def test_initializer_raises_ValueError_when_nameNotString(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Customer(100, VALID_EMAIL)

    def test_initializer_raises_ValueError_when_nameTooShort(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Customer(INVALID_NAME, VALID_EMAIL)

    def test_initializer_raises_ValueError_when_nameTooLong(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Customer(INVALID_NAME * 100, VALID_EMAIL)

    def test_initializer_raises_ValueError_when_emailNotString(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Customer(VALID_NAME, 100)

    def test_initializer_raises_ValueError_when_emailTooShort(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Customer(VALID_NAME, INVALID_EMAIL)

    def test_initializer_raises_ValueError_when_emailTooLong(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Customer(VALID_NAME, INVALID_EMAIL * 100)

    def test_initializer_raises_ValueError_when_emailNoAmpersant(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = Customer(VALID_NAME, INVALID_EMAIL_NO_AMP)

    def test_customerId_incrementsCorrectly(self):
        # ARRANGE + ACT
        customer1 = Customer(VALID_NAME, VALID_EMAIL)
        customer2 = Customer(VALID_NAME, VALID_EMAIL)
        self.assertGreater(customer2.id, customer1.id)

    def test_findPackageById_raises_ValueError_when_idNotFound(self):
        # AAA
        with self.assertRaises(ValueError):
            _ = VALID_CUSTOMER.find_package_by_id(100)

