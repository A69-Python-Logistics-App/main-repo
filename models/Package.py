from .Customer import Customer
from .Status import Status
from datetime import datetime

class Package():

    all_packages = []
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

        self._date_creation = datetime.now().strftime("%H:%M %d.%m.%Y") # time of package creation

        self._status = Status() # package status: Collected, On Route, Delivered
        
        # Append package to all packages - used for find_package_by_id
        Package.all_packages.append(self)


    def advance_package_status(self):
        """
        Advances package status.
        """
        self._status.advance_status()

    def find_package_by_id(self, id):
        """
        Tries to find package by id. Returns package_info()
        """
        for package in Package.all_packages:
            if package._id == id:
                return package.package_info()
        raise ValueError("Package not found!")

    def package_info(self):
        """
        Returns full package info.
        """
        return "\n".join([
            f"## Customer info: {self._contact.name}, {self._contact.email}",
            f"#  Package id: {self._id}, Status: {self._status.current}",
            f"# Package date creation: {self._date_creation}",
            f"#  Package pickup location: {self._pickup_loc}",
            f"#  Package current location: {self._current_loc}",
            f"#  Package destination: {self._dropoff_loc}",
            f"#  Package weight: {self._weight} KG"
        ])

    def realtime_info(self):
        """
        Currently returns self._current_loc ONLY.
        TODO: Time remaining until destination is reached. 
              Should also return more accurate current location.
        """
        return self._current_loc

# customer1 = Customer("Emanuil", "emko@abv.bg")
# package1 = Package(100, "Ruse", "Varna", customer1)
# package1.advance_package_status()
# print(package1.package_info())
# print(package1.find_package_by_id(1))