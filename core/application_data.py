from datetime import datetime, timedelta
from models.truck_carpark import TruckCarPark
from models.customer import Customer
from models.helpers import state
from models.location import Location
from models.package import Package
from models.route import Route
from models.status import Status
from models.user import User


class ApplicationData:

    HISTORY = "history.json"
    SYS_TIME_DEFAULT = "00:00 20.02.2025"

    def __init__(self):

        # Initiate log
        self._log = []

        # System time - default state at startup is always the same for now
        self._sys_time = datetime.strptime(self.SYS_TIME_DEFAULT, "%H:%M %d.%m.%Y")

        # Employees and current employee
        self._employees: list[User] = []
        self._current_employee: User | None = None

        # App data collections
        self._routes: list[Route] = []
        self._customers: list[Customer] = []
        self._packages: list[Package] = []

        # Initiate locations
        self._locations: list[Location] = [Location(loc) for loc in Location.cities]

    @property
    def customers(self) -> tuple:
        """
        Gets all customers in the system as Customer objects
        :return: tuple[Customer] - Customers as Customer objects
        """
        return tuple(self._customers)

    @property
    def packages(self) -> tuple:
        """
        Gets all packages in the system as Package objects
        :return: tuple[Package] - Packages as Package objects
        """
        return tuple(self._packages)

    @property
    def routes(self) -> tuple:
        """
        Gets all routes in the system as Route objects
        :return: tuple[Route] - Routes as Route objects
        """
        return tuple(self._routes)

    @property
    def current_employee(self) -> User | None:
        """
        Gets current employee as User object
        :return: User - Current employee as User object
        """
        return self._current_employee # Returns None if logged out

    @property
    def employees(self) -> tuple:
        """
        Returns a tuple with all employees as User objects
        :return: tuple[User] - Tuple with all employees
        """
        return tuple(self._employees)

    @property
    def log(self):
        """
        Returns a copy of the log
        :return: list - Log of all actions as copy
        """
        return self._log.copy()
    
    @property
    def system_time(self):
        """
        Returns system time, formatted in "%H:%M %d.%m.%Y"
        :return: datetime - Time 
        """
        return self._sys_time

    #
    # Write methods
    #


    # "00:00 20.02.2025"
    def fast_forward(self, num:int, type:str):
        """
        Fast forward system time by a given number of hours or days.
        
        :param num: int - The number of units to add.
        :param type: str - The type of units to add; either 'hours' or 'days'.
        :return: The updated system time as a string, or None if the type is invalid.
        """
        if type in ["hour", "hours"]:
            self._sys_time += timedelta(hours=num)
            self.process_deliveries()
            return f"System time is now: {self._sys_time}"
        elif type in ["day", "days"]:
            self._sys_time += timedelta(days=num)
            self.process_deliveries()
            return f"System time is now: {self._sys_time}"
        
        else:
            return None
        
        # TODO: fast_forward should call another function update_state or something, 
        # that must update all of the packages in the system that have an estimated time of arrival < or = to current sys time.

        

    def process_deliveries(self):
        print("Process_deliveries called")
        for route in self._routes:
            for stop in route.stops:
                delivered_packages = route.deliver_packages(stop)
                for package in delivered_packages:
                    print(f"Package #{package.id} delivered at {stop}.")
                    self.log_entry(f"Package #{package.id} delivered at {stop}.")

    def create_employee(self, username: str, password: str, role:str, login: bool=False) -> User:
        """
        Creates a new employee
        :param username: str - Username
        :param password: str - Password
        :param role: str - Role
        :param login: bool - Login employee after creation
        :return: User - New employee object
        """
        employee = User(username, password, role)
        self._employees.append(employee)
        if not self.current_employee and login:
            self._current_employee = employee
            self._login()
        return employee

    def create_package(self, weight, pickup, dropoff, customer_id) -> Package:
        package = Package(weight, pickup, dropoff, customer_id, self.system_time)
        self._packages.append(package)

        hub = self.find_hub_by_city(pickup)
        hub.list_of_packages_on_location.append(package.id)

        customer = self.find_customer_by_id(customer_id)
        customer.add_package(package.id)

        return package

    def remove_package(self, package: Package) -> str:
        # TODO: finish implementation

        # Check if package is not on route or delivered
        match package.status:
            case "On Route": # TODO: Make statuses accessible outside Status class
                raise ValueError(f"Package #{package.id} is on route and can no longer be removed!")
            case "Delivered": # Reject deletion of delivered package
                raise ValueError(f"Package #{package.id} has already been delivered and can not be removed from history!")

        customer = self.find_customer_by_id(package.customer_id)
        hub = self.find_hub_by_city(package.current_location)
        # customer.remove_package(package) TODO: add remove_package command to customer
        # hub.remove_package(package) TODO: look into hub implementation
        self._packages.remove(package)
        output = f"Package #{package.id} removed, updated customer #{customer.id} and hub [{hub.hub_name}]."
        del package # Remove from memory
        return output

    def create_route(self, date: datetime, locations: tuple) -> Route:
        route = Route(locations, date)
        self._routes.append(route)
        return route

    def remove_route(self, route: Route) -> str:
        unassigned = total_weight = 0
        # Change assigned packages to unassigned
        for package in route.list_of_packages: # TODO: Decide whether route contains IDs or Package objects
            package.status = "Collected" # TODO: Add reverse_status method to Status class
            total_weight += package.weight
            unassigned += 1

        id_number = route.route_id

        # Remove route from app data
        self._routes.remove(route)
        del route

        return f"Route #{id_number} removed, with {unassigned} packages (weighting a total of {total_weight}kg) unassigned."

    def create_customer(self, first_name: str, last_name: str, email: str) -> Customer:
        customer = Customer(first_name, last_name, email)
        self._customers.append(customer)
        return customer

    def remove_customer(self, customer: Customer) -> str:
        # TODO: Check if customer can be removed (unable to if customer has packages on route or delivered)
        self._customers.remove(customer)
        id_number= customer.id
        del customer
        return f"Customer #{id_number} removed."

    #
    # Read methods
    #

    def find_employee_by_username(self, username: str) -> User | None:
        """
        Find employee by username
        :param username: str - Username
        :return: Employee | None
        """
        for employee in self._employees:
            if employee.username == username:
                return employee


    def find_customer_by_email(self, email: str) -> Customer | None:
        """
        Find customer by email
        :param email: str - Email
        :return: Customer | None
        """
        for customer in self._customers: # Search by email for existing customer
            if customer.email == email:
                return customer

    def find_customer_by_id(self, id_number: int) -> Customer | None:
        """
        Find customer by id
        :param id_number: int - ID
        :return: Customer | None
        """
        for customer in self._customers: # Search by id for existing customer
            if customer.id == id_number:
                return customer

    def find_package_by_id(self, id_number: int) -> Package | None:
        """
        Find package by id
        :param id_number: int - ID
        :return: Package | None
        """
        for package in self._packages:
            if package.id == id_number:
                return package

    def find_route_by_id(self, id_number: int) -> Route | None:
        """
        Find route by id
        :param id_number: int - ID
        :return: Route | None
        """
        for route in self._routes:
            if route.route_id == id_number:
                return route

    def find_route_by_locations(self, pickup_location, dropoff_location) -> Route | None:
        for route in self._routes:
            if pickup_location in route.stops and dropoff_location in route.stops:
                if route.stops.index(dropoff_location) > route.stops.index(pickup_location):
                    return route
        return None


    def find_hub_by_city(self, city: str) -> Location | None:
        """
        Find hub by city
        :param city: str - City
        :return: Location | None
        """
        for location in self._locations:
            if location.hub_name == city:
                return location

    def find_packages_at_hub(self, hub: str) -> list[Package]:
        """
        Find packages at hub
        :param hub: str - City
        :return: list[Package]
        """
        packages_at_hub = []
        for package in self._packages:
            if package.status == Status.STATUSES[0] and package.current_location == hub:
                packages_at_hub.append(package)
        return packages_at_hub

    def find_routes_for_package(self, package_id: int) -> str:
        """
        Find routes for package
        :param package_id: int - ID
        :return: str - List of routes
        """
        package = self.find_package_by_id(package_id)
        routes = []
        for route in self.routes:
            if route.weight_capacity is None:
                continue
            if route.weight_capacity >= package.weight and route.current_weight + package.weight <= route.weight_capacity:
                routes.append(route)
        if routes:
            routes_info = "\n".join(str(route) for route in routes)
        else:
            routes_info = "No routes are available for this package"
        return routes_info

    def get_location_capacity(self, hub: str, date: datetime) -> int:
        """
        Get location capacity
        :param hub: str - City
        :param date: datetime - Date of inquiry
        :return: int - Capacty in kg
        """
        loc = self.find_hub_by_city(hub)
        # TODO: Implement getting hub trucks capacity
        return 0

    #
    # Action methods
    #

    def log_entry(self, entry: str) -> None:
        """
        Log operation entry
        :param entry: str - Log message
        :return: None
        """
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log.append(f"[{date}][{None if not self.current_employee else self.current_employee.username}] {entry}")

    def assign_package_to_route(self, package_id, route_id) -> None:
        """
        Assign package to route
        :param package_id: int - Package id
        :param route_id: int - Route id
        :return: None
        """
        package: Package = self.find_package_by_id(package_id)
        route: Route = self.find_route_by_id(route_id)
        if package.pickup_location not in route.stops or package.dropoff_location not in route.stops:
            raise ValueError("Package pick up location or drop off location not in this route")
        if route.stops.index(package.dropoff_location) < route.stops.index(package.pickup_location):
            raise ValueError("Drop off location has to be after the pick up location")
        if route.weight_capacity < package.weight or route.current_weight + package.weight > route.weight_capacity:
            raise ValueError("Not enough capacity for this package")
        else:
            route.list_of_packages.append(package)
            route.current_weight += package.weight

    def bulk_assign(self, hub: str, route: int) -> str:
        """
        TODO
        :param hub: Location/Hub
        :param route: int - Route id
        :return: str - Result of operation
        """
        packages = self.find_packages_at_hub(hub)
        route = self.find_route_by_id(route)
        assigned = 0
        for package in packages:
            # TODO: check if package is already assigned
            try:
                self.assign_package_to_route(package.id, route.route_id)
                assigned += 1
            except ValueError:
                continue
        return f"A total of {assigned} packages assigned to route #{route.route_id} ({len(packages) - assigned} packages remaining)."

    def update_customer(self, customer: Customer, new_first_name: str, new_last_name: str) -> str:
        """
        Updates customer name
        :param customer: Customer - Customer
        :param new_first_name: First name
        :param new_last_name: Last name
        :return: str - Result of operation
        """
        old_name = customer.first_name + " " + customer.last_name
        customer._first_name = new_first_name # TODO: Add setter for customer.first_name
        customer._last_name = new_last_name # TODO: Add setter for customer.last_name
        new_name = customer.first_name + " " + customer.last_name
        return f"Updated customer [{customer.email}] name from {old_name} to {new_name}."

    def reset_app(self) -> None:
        """
        Wipes out the app state data and exits the app.
        :return:  None
        """
        self.log_entry(f"Employee [{self.current_employee.username}] initiated system reset.")
        self._wipe()

    def logout(self) -> None:
        """
        Logs out the current employee.
        :return: None
        """
        self._current_employee = None

    def employee_login(self, username: str, password: str) -> None:
        """
        Authenticate an employee.

        :param username: The username of the employee attempting to log in.
        :param password: The password of the employee attempting to log in.
        :raises ValueError: If the credentials are invalid.
        """
        if not self._employees:
            raise ValueError("No employees registered.")

        if all(employee.username != username or employee.password != password for employee in self._employees):
            raise ValueError("Invalid credentials, try again.")

        # If we've reached this point, the credentials must be valid for at least one employee
        self._current_employee = self.find_employee_by_username(username)

    def ask_for_credentials(self, role: str) -> list[str]:
        """
        Internal method: asks for username and password for employee login/registration
        :param role: the current employee role
        :return: ['username', 'password']
        """
        command = input(f"{role} > ")
        if command == "exit":
            self.log_entry("System exited.")
            state.dump_to_file(self)
            exit("System exited.")
        if command.count(" ") != 1:
            raise ValueError("Invalid parameters, two expected - username and password separated by space!")
        return command.split()

    def login(self) -> bool:
        """
        Attempts to log into employee account or create one if none exist.
        ! Endless loop until user loggs in or types "exit"
        :return: bool - True if logged in
        """
        while not self.current_employee:
            # repeat until the user logs in an employee
            # check if there are employee accounts:
            while not len(self.employees):
                try:
                    # ask user to make an employee account until it's valid
                    username, password = self.ask_for_credentials("Create admin")

                    self.create_employee(username, password, User.ADMIN, True)
                    self.log_entry(f"Employee {self.current_employee.username} created and logged in")
                    return True
                except Exception as e:
                    self.log_entry(e.args[0])
                    print(e.args[0])
                    continue

            if self.current_employee:
                return True

            # There is at least one employee account
            try:
                username, password = self.ask_for_credentials("Login")
                self.employee_login(username, password)
                self.log_entry(f"Employee {username} logged in")
                return True
            except ValueError as e:
                self.log_entry(e.args[0])
                print(e.args[0])
                continue

    def update_employee_role(self, employee: str, role: str) -> str:
        employee = self.find_employee_by_username(employee)
        old_role = employee.role
        employee.role = role
        return f"Updated employee '{employee.username}' from role {old_role.upper()} to {role.upper()}."
    
    def update_employee_name(self, employee: str, new_name: str) -> str:
        employee = self.find_employee_by_username(employee)
        old_name = employee.username
        employee.username = new_name
        return f"Updated employee username from '{old_name}' to '{new_name}'."
    
    def update_employee_password(self, employee: str, new_password: str) -> str:
        employee = self.find_employee_by_username(employee)
        # old_password = employee.password
        employee.password = new_password
        return f"Updated the password of employee '{employee.username}'."
    
    def remove_employee(self, employee: str):
        employee = self.find_employee_by_username(employee)
        self._employees.remove(employee)
        return f"Employee '{employee.username}' has been removed."
    
    def view_routes(self) -> str:
        return "\n".join(str(route) for route in self._routes)

    def view_packages(self) -> str:
        return "\n".join(str(package) for package in self._packages)

    def view_trucks(self) -> str:
        return "\n".join(str(truck) for truck in TruckCarPark.list_all_free_trucks())

    #
    # Protected methods
    #

    def _login(self) -> None:
        """
        Log login
        :return: None
        TODO: Maybe not needed
        """
        if not self._current_employee:
            raise ValueError("self._login called when there is no current employee set.")
        return f"User {self.current_employee.username} logged in."

    def _wipe(self) -> None:
        """
        Wipes out the app state data and ends the application
        :return: None
        """
        self._customers.clear()
        self._packages.clear()
        self._routes.clear()
        self._locations.clear()
        self._employees.clear()
        self._log.clear()
        state.dump_to_file(self)
        exit("System reset.")

    #
    # Dunder methods
    #

    def __str__(self) -> str:
        """
        Formats app_data into a readable string
        :return: str - App data formatted
        """
        # TODO: Finish __str__() implementation
        return "\n".join([f"System has {len(self._customers)} customers with a total of {len(self._packages)} packages.",
                         f"Currently there are {len(self._routes)} routes between {len(self._locations)} locations."])