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
        self._packages:list[Package] = []
        self._id = Customer.__ID
        Customer.__ID += 1

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
    #asd
        
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
    def packages(self):
        """
        Return tuple with current customer's packages.
        """
        return tuple(self._packages)

    def add_package(self, package:Package):
        """
        Add a package to the customer's packages. Checks if package is type Package.
        """
        if type(package) != Package:
            raise ValueError(f"Method add_package accepts type Package only! You entered type {type(package)}.")
        self._packages.append(package)

    
    def find_package_by_id(self, id:int) -> Package:
        """
        Tries to find customer's package by id. Raise ValueError if not found.
        """
        for package in self._packages:
            if package.id == id:
                return package
        raise ValueError(f"Package with #{id} not found!")
    
    def info_package_by_id(self, id:int):
        """
        Uses find_package_by_id. Returns formatted string with current customer and package info.
        """
        package = self.find_package_by_id(id)
        return "\n".join([
            f"## Customer info: {self.first_name} {self.last_name}, {self.email}",
            f"#  Package id: {package.id}, Status: {package.status}",
            f"#  Package date creation: {package.date_creation}",
            f"#  Package pickup location: {package.pickup_location}",
            f"#  Package current location: {package.current_location}",
            f"#  Package destination: {package.dropoff_location}",
            f"#  Package weight: {package.weight} KG"
        ])

    def info_all_packages(self):
        """
        Returns formatted string with current customer and all packages info.
        """
        package_infos = [
            f"## Customer info: {self.first_name} {self.last_name}, {self.email}"
        ]

        if len(self._packages) == 0:
            return package_infos.append(f"#  CUSTOMER HAS NO PACKAGES.")
        
        else:
            for package in self._packages:
                package_infos.append("\n".join([
                    f"#  Package id: {package.id}, Status: {package.status}",
                    f"#  Package date creation: {package.date_creation}",
                    f"#  Package pickup location: {package.pickup_location}",
                    f"#  Package current location: {package.current_location}",
                    f"#  Package destination: {package.dropoff_location}",
                    f"#  Package weight: {package.weight} KG"
                ]))
            return "\n\n".join(package_infos)

    @classmethod
    def set_internal_id(cls, idn: int):
        """
        Set class __ID to the given value.
        """
        cls.__ID = idn