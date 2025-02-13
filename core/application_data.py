import json
from datetime import datetime

from models.customer import Customer
from models.location import Location
from models.package import Package
from models.route import Route
from models.status import Status
from models.user import User


class ApplicationData:

    HISTORY = "history.json"

    def __init__(self):

        # TODO: Implement employee login and permissions
        self._employees: [User] = []
        self._current_employee = None


        # TODO: Implement collections
        self._routes = []
        self._customers = []
        self._packages = []
        self._locations = [] # TODO: At start trucks won't have assigned locations, so they can be deployed immediately for their first ride

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
        return self._current_employee

    #
    # Write methods
    #

    def create_package(self, weight, pickup, dropoff, customer_id) -> str:
        package = Package(weight, pickup, dropoff, customer_id)
        self._packages.append(package)

        customer = self.find_customer_by_id(customer_id)
        customer.add_package(package) # find customer and add package

        return f"Package #{package.id} created and added to customer #{customer_id}."

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

    def create_route(self, date: datetime, *locations: list[str]) -> str:
        # TODO: fix implementation with the correct location validation
        try:
            route = Route(locations, date)
        except Exception as e:
            return e.args[0]

        self._routes.append(route)
        return f"Created route #{route.route_id} from {locations[0]} to {locations[-1]} with {len(locations) - 2} stops in-between created."

    def remove_route(self, route: Route) -> str:
        unassigned = total_weight = 0
        # Change assigned packages to unassigned
        for package in route.packages: # TODO: Decide whether route contains IDs or Package objects
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

    def find_customer_by_email(self, email: str) -> Customer | None:
        for customer in self._customers: # Search by email for existing customer
            if customer.email == email:
                return customer

    # TODO: Change customer identification to email
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
            # TODO: Make statuses accessible outside Status class
            if package.status == Status._class_status_types[0] and package.current_location == hub:
                packages_at_hub.append(package)
        return packages_at_hub

    def find_routes_for_package(self, package_id: int) -> list[Route]:
        package: Package = self.find_package_by_id(package_id)
        routes: list[Route] = []
        # TODO: Implement finding routes for package
        return routes

    def get_location_total_package_weight(self, hub: str) -> int:
        loc = self.find_hub_by_city(hub)
        # TODO: Implement getting hub trucks capacity
        # Ignore packages that are not at hub or delivered (Status: On Route/Delivered)
        return 0

    #
    # Action methods
    #

    def assign_package_to_route(self, package_id: int, route_id: int) -> None:
        package: Package = self.find_package_by_id(package_id)
        route: Route = self.find_route_by_id(route_id)
        # TODO: Implement assigning package to route
        # Check weight capacity

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
        self._wipe()

    #
    # Dunder methods
    #

    def _wipe(self):
        proceed = True
        if input("!> If you proceed, all data will be permanently lost. (y/n): ").lower() != "y":
            proceed = False
        elif input("!!!> Final confirmation (y/n): ").lower() != "y":
            proceed = False

        if not proceed:
            raise ValueError("System reset cancelled.")

        self._customers.clear()
        self._packages.clear()
        self._routes.clear()
        self._locations.clear()
        self._employees.clear()
        raise SystemExit("System reset finished successfully.")

    def __str__(self):
        # TODO: Finish __str__() implementation
        return "\n".join([f"System has {len(self._customers)} customers with a total of {len(self._packages)} packages.",
                         f"Currently there are {len(self._routes)} routes between {len(self._locations)} locations."])


    #
    # File I/O
    #

    def dump_state_to_app(self) -> str:
        # customers, packages, routes, locations, log
        # TODO: Import self.HISTORY file and parse data into objects for ApplicationData
        with open(self.HISTORY, "r") as f:
            state = json.load(f)
            state = dict()
            if not state.get("customers"): # there is no history.json file, or it is empty/unreadable
                return "There is no application data history to load from."

        # Customer unpacking
        # customers[id_number]: data
        max_customer_id = 0
        for id_number, customer in state["customers"].items():
            id_number = int(id_number)
            c = self.create_customer(customer["first_name"], customer["last_name"], customer["email"])
            c._id = id_number
            max_customer_id = max(id_number, max_customer_id)
        c.set_internal_id(max_customer_id + 1) # TODO: Make Customer.set_internal_id class method

        # TODO: Implements packages, routes, locations/hubs unpacking

        return "Application Data history loaded from local storage."

    def dump_state_to_file(self, log: [str]):
        # TODO: Finish implementation for saving app state
        state: dict[str:dict] = {
            "customers": {},
            "packages": {},
            "routes": {},
            "locations": {},
            "log": log
        }

        for customer in self._customers:
            state["customers"][customer.id] = { # TODO: Customer ID is string
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                # TODO Issue:
                # customer1 = Customer("Siso", "siso@icloud.com")
                # customer1 packages = [package1, package2, package3, package4]
                # packages are Package objects and cannot be stored in a JSON file
                # Solution 1: store packages in Customer object as a list of package IDs
                # Solution 2: store package IDs in history and hardcode the re-population of packages by ID
                "packages": []
            }

        for package in self._packages:
            state["packages"][package.id] = {
                "weight": package.weight,
                "pickup": package.pickup_location,
                "dropoff": package.dropoff_location,
                "customer_id": package.customer_id,
                "status": package.status,
                "current_loc": package.current_location,
                "date_creation": package.date_creation
            }

        for route in self._routes: # TODO: Add route getters and an ID setter for initialization from history
            state["routes"][route.route_id] = {
                "stops": route.stops,
                "takeoff": datetime.now().isoformat() # TODO: Route doesn't have takeoff time getter
            }

        for location in self._locations:
            state["locations"][location.hub_name] = { # TODO: Review locations implementation
                "name": location.hub_name,
                "trucks": [] # TODO: Maybe?
            }

        with open(self.HISTORY, "w") as f:
            json.dump(state, f)