from datetime import datetime
from models.helpers.validation_helpers import parse_to_int

class Package():

    __ID = 1000

    __STATUSES = ["Collected", "Loaded", "On Route", "Delivered"]

    def __init__(self, weight:int, pickup_loc:str, dropoff_loc:str, customer_id:int, date_creation:datetime):

        """
        Package with weight, pickup location, dropoff location and customer id. Contains current location, \n
        date of creation, status and a sequential id, starting from 1000.
        """

        if weight < 0:
            raise ValueError("Package weight cannot be < 0!")
        self._weight = weight # weight in KGs

        self._pickup_loc = pickup_loc # pickup location
        self._dropoff_loc = dropoff_loc # dropoff location
        self._current_loc = self._pickup_loc # DEFAULT current location: at pickup

        self._date_creation = date_creation # time of package creation - Sys time
        self._status = Package.__STATUSES[0] # default value

        # Set package id and increment
        self._package_id = Package.__ID
        Package.__ID += 1

        self._customer_id = customer_id

    @classmethod
    def set_internal_id(self, ID:int):
        """
        Set class __ID to the given value.
        """
        num = parse_to_int(ID)
        if num < 0:
            raise ValueError("ID cannot be below zero!")
        Package.__ID = num

    @property
    def id(self):
        """
        Return current package id.
        """
        return self._package_id
    
    @property
    def customer_id(self):
        """
        Return current package's customer id.
        """
        return self._customer_id

    @property
    def status(self):
        """
        Return current package status.
        """
        return self._status
    
    @property
    def weight(self):
        """
        Return package weight.
        """
        return self._weight

    @property
    def pickup_location(self):
        """
        Return package pickup location.
        """
        return self._pickup_loc

    @property
    def dropoff_location(self):
        """
        Return package dropoff location.
        """
        return self._dropoff_loc

    @property
    def current_location(self):
        """
        Return current package location.
        """
        return self._current_loc

    @property
    def date_creation(self):
        """
        Return creation date of package. Formatted in "hours:minutes day.month.year".
        """
        return self._date_creation

    @current_location.setter
    def current_location(self, location:str):
        """
        Set current package location.
        """
        self._current_loc = location

    def update_status(self, status:str):
        """
        Update status to given string. Raise ValueError if string not in "Collected", "Loaded", "On Route", "Delivered".
        """
        if status not in Package.__STATUSES:
            raise ValueError("Invalid package status")
        self._status = status

    def update_location(self, new_location:str):
        self._current_loc = new_location