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
        self._employees: list[User] = []
        self._current_employee = None


        # TODO: Implement collections
        self._routes = []
        self._customers = []
        self._packages = []
        self._locations = [] # TODO: At start trucks won't have assigned locations, so they can be deployed immediately for their first ride

        self._locations = [Location(loc) for loc in Location.Cities] # TODO: init locations from cities or change locations implementation

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
    def employee(self) -> User | None:
        return self._current_employee

    def create_package(self, weight, pickup, dropoff, customer_id) -> str:
        package = Package(weight, pickup, dropoff, customer_id)
        self._packages.append(package)

        customer = self.find_customer_by_id(customer_id)
        customer.add_package(package) # find customer and add package

        return f"Package #{package.id} created and added to customer #{customer_id}."

    def create_route(self, date: datetime, *locations: list[str]) -> str:
        # TODO: fix implementation with the correct location validation
        try:
            route = Route(locations, date)
        except Exception as e:
            return e.args[0]

        self._routes.append(route)
        return f"Route #{route.route_id} from {locations[0]} to {locations[-1]} with {len(locations) - 2} stops created."

    def create_customer(self, first_name: str, last_name: str, email: str) -> Customer:
        customer = Customer(first_name, last_name, email)
        self._customers.append(customer)
        return customer

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
            if package.status == Status._class_status_types[0] and package.current_location == hub:
                packages_at_hub.append(package)
        return packages_at_hub

    def find_routes_for_package(self, package_id: int) -> list[Route]:
        package: Package = self.find_package_by_id(package_id)
        routes: list[Route] = []
        # TODO: Implement finding routes for package
        # TODO: return formatted string
        return routes

    def assign_package_to_route(self, package_id, route_id) -> None:
        package: Package = self.find_package_by_id(package_id)
        route: Route = self.find_route_by_id(route_id)
        # TODO: Implement assigning package to route
        # Check weight capacity

    def get_location_capacity(self, hub: str, date: datetime) -> int:
        loc = self.find_hub_by_city(hub)
        # TODO: Implement getting hub trucks capacity
        return 0

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

    #
    # Saving app state to file
    #

    def __str__(self):
        # TODO: Finish __str__() implementation
        return "\n".join([f"System has {len(self._customers)} customers with a total of {len(self._packages)} packages.",
                         f"Currently there are {len(self._routes)} routes between {len(self._locations)} locations."])

    def state_dump(self, state: dict[str:dict]):
        # customers, packages, routes, locations, log
        pass

    def init_from_history(self):
        # TODO: Implement loading app state from history
        pass

    def save_state_to_history(self, log: list[str]):
        # TODO: Finish implementation for saving app state
        state: dict[str:dict] = {
            "customers": {},
            "packages": {},
            "routes": {},
            "locations": {},
            "log": log
        }

        for customer in self._customers:
            state["customers"][customer.id] = {
                "name": customer.name,
                "email": customer.email,
                "packages": customer.packages # TODO: customer.packages should be a list of int
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

        for route in self._routes:
            state["routes"][route.route_id] = {
                "locations": route.stops,
                "date": datetime.now().isoformat() # TODO: Route doesn't have creation date getter
            }

        for location in self._locations:
            state["locations"][location.id] = { # TODO: Review locations implementation
                "name": location.name,
                "location": location.location
            }

        with open(self.HISTORY, "w") as f:
            json.dump(state, f)