
# It looks like the issue lies within your Customer class definition. 
# The _check_valid_name and _check_valid_email methods should be defined 
# as @staticmethod since you're calling them on the class itself rather than on an instance of the class.

class Customer:
    def __init__(self, name:str, email:str):
        self.name = Customer._check_valid_name(name)
        self.email = Customer._check_valid_email(email)
        self.package_id = "UNKNOWN" # default package id is unknown, Package sets id

    @staticmethod
    def _check_valid_name(name):
        """
        Validate name. Checks for type and lenght.
        """
        if type(name) != str:
            raise ValueError("Name must be a string!")
        if len(name) < 3 or len(name) > 15:
            raise ValueError("Name lenght error!")
        return name
        
    @staticmethod
    def _check_valid_email(email):
        """
        Validate email. Checks for type, lenght and @.
        """
        if type(email) != str:
            raise ValueError("Email must be a string!")
        if len(email) < 3 or len(email) > 20:
            raise ValueError("Email lenght error!")
        if "@" not in email:
            raise ValueError("Email must contain a '@'!")
        return email

    def set_package_id(self, id:int): # set package id
        if type(id) != int:
            raise ValueError("Id must be an integer!")
        self.package_id = id