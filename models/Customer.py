from Package import Package

class Customer:

    _customer_id = 1

    def __init__(self, name:str, email:str):
        
        self._name = Customer._check_valid_name(name)
        self._email = Customer._check_valid_email(email)
        self._packages:list[Package] = []
        self._id = Customer._customer_id
        Customer._customer_id += 1

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
        Return current customer's name.
        """
        return self._name

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
            f"## Customer info: {self.name}, {self.email}",
            f"#  Package id: {package.id}, Status: {package.status}",
            f"#  Package date creation: {package._date_creation}",
            f"#  Package pickup location: {package._pickup_loc}",
            f"#  Package current location: {package._current_loc}",
            f"#  Package destination: {package._dropoff_loc}",
            f"#  Package weight: {package.weight} KG"
        ])

    def info_all_packages(self):
        """
        Returns formatted string with current customer and all packages info.
        """
        package_infos = [
            f"## Customer info: {self.name}, {self.email}"
        ]

        if len(self._packages) == 0:
            return package_infos.append(f"#  CUSTOMER HAS NO PACKAGES.")
        
        else:
            for package in self._packages:
                package_infos.append("\n".join([
                    f"#  Package id: {package.id}, Status: {package.status}",
                    f"#  Package date creation: {package._date_creation}",
                    f"#  Package pickup location: {package._pickup_loc}",
                    f"#  Package current location: {package._current_loc}",
                    f"#  Package destination: {package._dropoff_loc}",
                    f"#  Package weight: {package.weight} KG"
                ]))
            return "\n\n".join(package_infos)
        
# customer1 = Customer("Emanuil", "emko@abv.bg")
# package1 = Package(100, "Ruse", "Varna", customer1.id)
# customer1.add_package(package1)
# customer1.add_package(package1)
# customer1.add_package(package1)
# customer1.add_package(package1)

# package1.advance_package_status()
# print(customer1.info_package_by_id(customer1.id))
# print(customer1.info_all_packages())