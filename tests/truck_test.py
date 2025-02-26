import unittest
from models.truck import Truck

class TruckShould(unittest.TestCase):

    def test_reset_sets_truck_to_default_location_and_free(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)
        truck._current_location = "...."  
        truck._is_free = False
    
        truck.reset()  

        self.assertEqual(truck._current_location, "Car Park")  
        self.assertTrue(truck._is_free)  


    def test_is_free_only_boolean(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)

        truck.is_free = False
        self.assertFalse(truck.is_free)
        truck.is_free = True
        self.assertTrue(truck.is_free)

    def test_is_free_raises_value_error_when_not_boolean(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)

        with self.assertRaises(ValueError):
            truck.is_free = "abv"
        with self.assertRaises(ValueError):
            truck.is_free = 1
        with self.assertRaises(ValueError):
            truck.is_free = None
    
    def test_current_location_valid_type(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)
        valid_location = "SYD"

        truck.current_location = valid_location
        self.assertEqual(truck.current_location, valid_location)
    
    def test_current_location_invalid_type(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)

        with self.assertRaises(ValueError):
            truck.current_location = 1
        with self.assertRaises(ValueError):
            truck.current_location = None
        with self.assertRaises(ValueError):
            truck.current_location = True
    
    def test_truck_correct_initialization(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)
        self.assertEqual(truck.name, "TestTruck")
        self.assertEqual(truck.id, 1)
        self.assertEqual(truck.capacity, 40_000)
        self.assertEqual(truck.range, 8000)
        self.assertEqual(truck.current_location, "Car Park")
        self.assertTrue(truck.is_free)
    
    def test_truck_attributes_can_not_change(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)
        with self.assertRaises(AttributeError):
            truck.name = "MAN"
        with self.assertRaises(AttributeError):
            truck.id = 2
        with self.assertRaises(AttributeError):
            truck.capacity = 50_000
        with self.assertRaises(AttributeError):
            truck.range = 9000
    
    def test_string_representation(self):
        truck = Truck("TestTruck", 1, 40_000, 8000)
        valid_str = "#1 TestTruck : capacity: 40000kg, range: 8000km | Free: True | Location in Car Park"
        self.assertEqual(str(truck), valid_str)
        

        