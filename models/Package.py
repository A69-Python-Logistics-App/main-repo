from Status import Status
from datetime import datetime

class Package():

    _class_all_packages = []

    def __init__(self, weight:int, pickup_loc:str, dropoff_loc:str, customer_id:int):

        if weight < 0:
            raise ValueError("Package weight cannot be < 0!")
        self._weight = weight # weight in KGs

        self._pickup_loc = pickup_loc # pickup location
        self._dropoff_loc = dropoff_loc # dropoff location
        self._id = customer_id

        self._current_loc = self._pickup_loc # DEFAULT current location: at pickup
        self._date_creation = datetime.now().strftime("%H:%M %d.%m.%Y") # time of package creation
        self._status = Status() # package status: Collected, On Route, Delivered
        
        # Append package to all packages - could be used for something
        Package._class_all_packages.append(self)

    @property
    def id(self):
        """
        Return package id.
        """
        return self._id
    
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

    # def realtime_info(self):
    #     """
    #     Currently returns self._current_loc and creation date ONLY.\n
    #     TODO: Time remaining until destination is reached. 
    #     Should also return more accurate current location.
    #     """
    #     return "\n".join([
    #         f"# Package current location: {self._current_loc}",
    #         f"# Package creation date: {self._date_creation}"
    #     ])