import unittest
from models.customer import Customer
from models.helpers.validation_helpers import parse_to_int

class TestCustomer(unittest.TestCase):

    def setUp(self):
        # Reset the internal ID before each test
        Customer.set_internal_id(1)

    def test_set_internal_id_valid(self):
        Customer.set_internal_id(10)
        customer = Customer("John", "Doe", "john.doe@example.com")
        self.assertEqual(customer.id, 10)

    def test_set_internal_id_invalid_non_integer(self):
        with self.assertRaises(ValueError):
            Customer.set_internal_id("invalid")

    def test_set_internal_id_invalid_negative_integer(self):
        with self.assertRaises(ValueError):
            Customer.set_internal_id(-5)