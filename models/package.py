from models.status import Status
from datetime import datetime

class Package():

    _class_all_packages = []
    _customer_package_counts = {}

    def __init__(self, weight:int, pickup_loc:str, dropoff_loc:str, customer_id:int):

        """
        Package with weight, pickup location, dropoff location and customer id.
        """
        if weight < 0:
            raise ValueError("Package weight cannot be < 0!")
        self._weight = weight # weight in KGs

        self._pickup_loc = pickup_loc # pickup location
        self._dropoff_loc = dropoff_loc # dropoff location
        if type(customer_id) != int:
            raise ValueError("Invalid customer_id for package!")
        self._customer_id = customer_id
        
        if self._customer_id not in Package._customer_package_counts:
            Package._customer_package_counts[self._customer_id] = 1
        else:
            Package._customer_package_counts[self._customer_id] += 1

        self._package_id = Package._customer_package_counts[self._customer_id]

        self._current_loc = self._pickup_loc # DEFAULT current location: at pickup
        self._date_creation = datetime.now().strftime("%H:%M %d.%m.%Y") # time of package creation
        self._status = Status() # package status: Collected, On Route, Delivered
        
        # Append package to all packages - could be used for something
        Package._class_all_packages.append(self)


    @property
    def id(self):
        """
        Return package id for current customer.
        """
        return self._package_id
    
    
    @property
    def status(self):
        """
        Return current package status.
        """
        return self._status.current
    
    @property
    def weight(self):
        """
        Return package weight.
        """
        return self._weight
    def advance_package_status(self):
        """
        Advances package status.
        """
        self._status.advance_status()

package1 = Package(10, "Location A", "Location B", 1)
package2 = Package(15, "Location A", "Location B", 1)
package3 = Package(20, "Location A", "Location B", 1)
print(package1.id)  # Output: 1 - 1
print(package2.id)  # Output: 1 - 2
print(package3.id)  # Output: 1 - 3
print()

package4 = Package(10, "Location A", "Location B", 2)
package5 = Package(15, "Location A", "Location B", 3)
package6 = Package(20, "Location A", "Location B", 3)

print(package4.id)  # Output: 1 - 1
print(package5.id)  # Output: 1 - 2
print(package6.id)  # Output: 1 - 3
print()