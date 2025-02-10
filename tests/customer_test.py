import unittest
from models.Customer import Customer

VALID_NAME = "EMKO"
VALID_EMAIL = "emko@abv.bg"
VALID_ID = 1
INVALID_ID = -100

INVALID_NAME = "E"
INVALID_EMAIL = "E@BG"
INVALID_EMAIL_NO_AMP = "EMKOABV.BG"

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

    def test_setPackageId_sets_packageId_when_validId(self):
        # ARRANGE
        customer = Customer(VALID_NAME, VALID_EMAIL)
        # ACT
        old_id = customer.package_id
        customer.set_package_id(VALID_ID)
        id = customer.package_id
        # ASSERT
        self.assertNotEqual(id, old_id)

    def test_setPackageId_raises_ValueError_when_idNotInteger(self):
        # ARRANGE
        customer = Customer(VALID_NAME, VALID_EMAIL)
        # ACT + ASSERT
        with self.assertRaises(ValueError):
            customer.set_package_id(INVALID_ID)

    def test_setPackageId_raises_ValueError_when_idBelowZero(self):
        # ARRANGE
        customer = Customer(VALID_NAME, VALID_EMAIL)
        # ACT + ASSERT
        with self.assertRaises(ValueError):
            customer.set_package_id(VALID_ID * -100)




