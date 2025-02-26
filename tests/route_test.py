import unittest
from models.route import Route
from models.helpers.validation_helpers import parse_to_int
from datetime import datetime

class TestRoute(unittest.TestCase):

    def setUp(self):
        # Reset the internal ID before each test
        Route.set_internal_id(1)

    def test_set_internal_id_valid(self):
        Route.set_internal_id(10)
        route = Route(("SYD", "MEL"), datetime.now())
        self.assertEqual(route.id, 10)

    def test_set_internal_id_invalid_non_integer(self):
        with self.assertRaises(ValueError):
            Route.set_internal_id("invalid")

    def test_set_internal_id_invalid_negative_integer(self):
        with self.assertRaises(ValueError):
            Route.set_internal_id(-5)