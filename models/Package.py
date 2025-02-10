from models.Customer import Customer
from models.Status import Status
from datetime import datetime

class Package():
    id = 1
    def __init__(self, weight:int, pickup_loc:str, dropoff_loc:str, contact: Customer):

        self._id = Package.id
        Package.id += 1 # increment id

        if weight < 0:
            raise ValueError("Package weight cannot be < 0!")
        self._weight = weight # weight in KGs

        self._pickup_loc = pickup_loc # pickup location
        self._dropoff_loc = dropoff_loc # dropoff location
        self._current_loc = self._pickup_loc # DEFAULT current location: at pickup

        self._contact = contact # Contact info
        self._contact.set_package_id(self._id)# set package id to customer

        self._date_creation = datetime.now() # time of package creation

        self._current_status = Status() # package status: Collected, On Route, Delivered

    def advance_package_status(self):
        self._current_status.advance_status()

    def find_package_by_id(self, id):
        pass

    def package_info(self):
        pass

    def realtime_info(self):
        return self._current_loc

        
customer1 = Customer("Emanuil", "emko@abv.bg")
package1 = Package(100, "Ruse", "Varna", customer1)