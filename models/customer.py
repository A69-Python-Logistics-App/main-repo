from models.package import Package

class Customer():

    __ID = 1

    def __init__(self, first_name:str, last_name:str, email:str):

        """ 
        Customer with first name, last name and email.
        Contains a list with packages, has a sequential id, starting from 1.
        """
        self._first_name = Customer._check_valid_name(first_name)
        self._last_name = Customer._check_valid_name(last_name)
        self._email = Customer._check_valid_email(email)
        self._package_ids:list[int] = []
        self._id = Customer.__ID
        Customer.__ID += 1

    @classmethod
    def set_internal_id(self, ID:int):
        """
        Set class __ID to the given value.
        """
        Customer.__ID = ID

    @staticmethod
    def _check_valid_name(name):
        """
        Validate name. Checks for type and lenght.
        """
        if type(name) != str:
            raise ValueError("Name must be a string!")
        if len(name) < 2 or len(name) > 12:
            raise ValueError("Name lenght error!")
        if not name.isalpha():
            raise ValueError("Name is not an alphabetic string!")
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
    def first_name(self):
        """
        Return current customer's first name.
        """
        return self._first_name
    
    @property
    def last_name(self):
        """
        Return current customer's last name.
        """
        return self._last_name

    @property
    def email(self):
        """
        Return current customer's email.
        """
        return self._email
    
    @property
    def id(self):
        """
        Return current customer's id.
        """
        return self._id
    
    @property
    def package_ids(self):
        """
        Return tuple with current customer's package ids.
        """
        return tuple(self._package_ids)

    def add_package(self, package_id:int):
        """
        Add a package id to the customer. Checks if package is type Package.
        """
        if type(package_id) != int:
            raise ValueError(f"Method add_package accepts type int only! You entered type {type(package_id)}.")
        self._package_ids.append(package_id)

    
    def find_package_by_id(self, package_id:int) -> bool:
        """
        Tries to find package id in current customer. Returns True/False.
        """
        for id in self._package_ids:
            if id == package_id:
                return True
        return False