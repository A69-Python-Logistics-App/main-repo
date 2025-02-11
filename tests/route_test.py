import unittest
from models.route import Route
from datetime import datetime, timedelta

class TestRout_Should(unittest.TestCase):
    def test_route_raises_error_when_stops_less_than_two(self):
        with self.assertRaises(ValueError):
            route = Route(stops=["SYD"], departure_time=datetime.now())
            

