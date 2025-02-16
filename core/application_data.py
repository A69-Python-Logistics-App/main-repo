from datetime import datetime

from models.customer import Customer
from models.helpers import state
from models.location import Location
from models.package import Package
from models.route import Route
from models.status import Status
from models.user import User


class ApplicationData:

    HISTORY = "history.json"

    def __init__(self):

        self._log = []

        # TODO: Implement employee login and permissions
        self._employees: list[User] = []
        self._current_employee = None

        # TODO: Implement collections
        self._routes: list[Route] = []
        self._customers: list[Customer] = []
        self._packages: list[Package] = []
        self._locations: list[Location] = []

        self._locations = [Location(loc) for loc in Location.cities] # TODO: init locations from cities or change locations implementation

    #
    # Properties
    #

    @property
    def customers(self) -> tuple:
        return tuple(self._customers)

    @property
    def packages(self) -> tuple:
        return tuple(self._packages)

    @property
    def routes(self) -> tuple:
        return tuple(self._routes)

    @property
    def current_employee(self) -> User | None:
        return self._current_employee # Returns None if logged out

    @property
    def employees(self) -> tuple:
        return tuple(self._employees)

    @property
    def log(self):
        return self._log.copy()

    #
    # Write methods
    #

    def create_employee(self, username: str, password: str, role:str, login: bool=False) -> User:
        employee = User(username, password, role)
        self._employees.append(employee)
        if not self.current_employee and login:
            self._current_employee = employee
            self._login()
        return employee
    
    def employee_login(self, username: str, password: str):
        validate = [not len(self._employees)]
        validate += [True for employee in self._employees if employee.username != username or employee.password != password]
        if any(validate):
            raise ValueError("Invalid credentials, try again.")

        employee = self.find_employee_by_username(username)
        self._current_employee = employee

    def create_package(self, weight, pickup, dropoff, customer_id) -> Package:
        package = Package(weight, pickup, dropoff, customer_id)
        self._packages.append(package)

        hub = self.find_hub_by_city(pickup)
        hub.list_of_packages_on_location.append(package.id)

        customer = self.find_customer_by_id(customer_id)
        customer.add_package(package.id) # find customer and add package id

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

    def create_route(self, date: datetime, *locations: list[str]) -> Route:
        # TODO: fix implementation with the correct location validation
        try:
            route = Route(locations[0], date)
        except Exception as e:
            return e.args[0]

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
        for employee in self._employees:
            if employee.username == username:
                return employee


    def find_customer_by_email(self, email: str) -> Customer | None:
        for customer in self._customers: # Search by email for existing customer
            if customer.email == email:
                return customer

    def find_customer_by_id(self, id_number: int) -> Customer | None:
        for customer in self._customers: # Search by id for existing customer
            if customer.id == id_number:
                return customer

    def find_package_by_id(self, id_number: int) -> Package | None:
        for package in self._packages:
            if package.id == id_number:
                return package

    def find_route_by_id(self, id_number: int) -> Route | None:
        for route in self._routes:
            if route.route_id == id_number:
                return route

    def find_hub_by_city(self, city: str) -> Location | None:
        for location in self._locations:
            if location.hub_name == city:
                return location

    def find_packages_at_hub(self, hub: str) -> list[Package]:
        packages_at_hub = []
        for package in self._packages:
            if package.status == Status.STATUSES[0] and package.current_location == hub:
                packages_at_hub.append(package)
        return packages_at_hub

    def find_routes_for_package(self, package_id: int) -> str:
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
        loc = self.find_hub_by_city(hub)
        # TODO: Implement getting hub trucks capacity
        return 0

    #
    # Action methods
    #

    def log_entry(self, entry: str) -> None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log.append(f"[{date}][{None if not self.current_employee else self.current_employee.username}] {entry}")

    def assign_package_to_route(self, package_id, route_id) -> None:
        package: Package = self.find_package_by_id(package_id)
        route: Route = self.find_route_by_id(route_id)
        if route.weight_capacity < package.weight or route.current_weight + package.weight > route.weight_capacity:
            raise ValueError("Not enough capacity for this package")
        else:
            route.list_of_packages.append(package)
            route.current_weight += package.weight

    def bulk_assign(self, hub: str, route: int) -> str:
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
        old_name = customer.first_name + " " + customer.last_name
        customer._first_name = new_first_name # TODO: Add setter for customer.first_name
        customer._last_name = new_last_name # TODO: Add setter for customer.last_name
        new_name = customer.first_name + " " + customer.last_name
        return f"Updated customer [{customer.email}] name from {old_name} to {new_name}."

    def reset_app(self):
        self.log_entry(f"Employee [{self.current_employee.username}] initiated system reset.")
        self._wipe()

    def logout(self) -> None:
        self._current_employee = None

    def employee_login(self, username: str, password: str):
        if not self._employees or all(
                employee.username != username or employee.password != password for employee in self._employees):
            raise ValueError("Invalid credentials, try again.")

        self._current_employee = self.find_employee_by_username(username)

    def ask_for_credentials(self, role: str) -> list[str]:
        command = input(f"{role} > ")
        if command == "exit":
            self.log_entry("System exited.")
            state.dump_to_file(self)
            exit("System exited.")
        if command.count(" ") != 1:
            raise ValueError("Invalid parameters, two expected - username and password separated by space!")
        return command.split()

    def login(self) -> bool:
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
        return f"Updated employee {employee.username} from {old_role} role to {role}."

    #
    # Dunder methods
    #

    def _login(self):
        if not self._current_employee:
            raise ValueError("self._login called when there is no current employee set.")
        return f"User {self.current_employee.username} logged in."

    def _wipe(self):
        self._customers.clear()
        self._packages.clear()
        self._routes.clear()
        self._locations.clear()
        self._employees.clear()
        self._log.clear()
        state.dump_to_file(self)
        exit("System reset.")

    def __str__(self):
        # TODO: Finish __str__() implementation
        return "\n".join([f"System has {len(self._customers)} customers with a total of {len(self._packages)} packages.",
                         f"Currently there are {len(self._routes)} routes between {len(self._locations)} locations."])