import unittest
from models.truck import Truck
from models.truck_car_park import TruckCarPark

class TestTruckCarPark(unittest.TestCase):

    def setUp(self):
        self.truck_car_park = TruckCarPark()

    def test_initialize_trucks(self):
        self.assertEqual(len(self.truck_car_park.trucks), 40)
        self.assertEqual(self.truck_car_park.trucks[0].name, TruckCarPark.SCANIA)
        self.assertEqual(self.truck_car_park.trucks[10].name, TruckCarPark.MAN)
        self.assertEqual(self.truck_car_park.trucks[25].name, TruckCarPark.ACTROS)

    def test_add_truck(self):
        truck = Truck(TruckCarPark.SCANIA, 1041, TruckCarPark.CAP_SCANIA, TruckCarPark.SCANIA_MAX_RANGE)
        self.truck_car_park.add_truck(truck)
        self.assertIn(truck, self.truck_car_park.trucks)

    def test_list_all_free_trucks(self):
        for truck in self.truck_car_park.trucks:
            truck.is_free = True
        free_trucks = self.truck_car_park.list_all_free_trucks()
        self.assertEqual(len(free_trucks), 40)

    def test_find_free_truck_by_name(self):
        for truck in self.truck_car_park.trucks:
            truck.is_free = True
        truck = self.truck_car_park.find_free_truck_by_name(TruckCarPark.SCANIA)
        self.assertEqual(truck.name, TruckCarPark.SCANIA)

    def test_find_truck_by_id(self):
        truck = self.truck_car_park.find_truck_by_id(1001)
        self.assertEqual(truck.id, 1001)