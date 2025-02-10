
# It looks like the issue lies within your Customer class definition. 
# The _check_valid_name and _check_valid_email methods should be defined 
# as @staticmethod since you're calling them on the class itself rather than on an instance of the class.

class Customer:
    def __init__(self, name:str, email:str):
        self._name = Customer._check_valid_name(name)
        self._email = Customer._check_valid_email(email)
        self._package_id = "UNKNOWN" # default package id is unknown, Package sets id

    @staticmethod
    def _check_valid_name(name):
        """
        Validate name. Checks for type and lenght.
        """
        if type(name) != str:
            raise ValueError("Name must be a string!")
        if len(name) < 4 or len(name) > 16:
            raise ValueError("Name lenght error!")
        return name
        
    @staticmethod
    def _check_valid_email(email):
        """
        Validate email. Checks for type, lenght and @.
        """
        if type(email) != str:
            raise ValueError("Email must be a string!")
        if len(email) < 5 or len(email) > 20:
            raise ValueError("Email lenght error!")
        if "@" not in email:
            raise ValueError("Email must contain a '@'!")
        return email

    @property
    def name(self):
        """
        Return customer name.
        """
        return self._name

    @property
    def email(self):
        """
        Return customer email.
        """
        return self._email

    @property
    def package_id(self) -> int:
        """
        Return customer's package id. Should return int, \n
        but could return "UNKNOWN" if id is not set.
        """
        return self._package_id

    def set_package_id(self, id:int):
        """
        Sets package id to the customer.
        """
        if type(id) != int:
            raise ValueError("Id must be an integer!")
        if id < 0:
            raise ValueError("Id must be a positive integer!")
        self._package_id = id