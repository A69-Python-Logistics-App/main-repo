import json
from datetime import datetime

from models.customer import Customer
from models.package import Package
from models.route import Route


class ApplicationData:

    HISTORY = "history.json"

    def __init__(self):
        # TODO: Implement collections
        self._routes = []
        self._customers = []
        self._packages = []
        self._locations = []

    @property
    def routes(self):
        return tuple(self._routes)

    def create_package(self, weight, pickup, dropoff, customer_id) -> str:
        package = Package(weight, pickup, dropoff, customer_id)
        self._packages.append(package)
        return f"Package #{package.id} created."

    def create_route(self, date: datetime, *locations: list[str]) -> str:
        # TODO: fix implementation with the correct location validation
        try:
            route = Route(locations, date)
        except Exception as e:
            return e.args[0]

        self._routes.append(route)
        return f"Route #{route.route_id} from {locations[0]} to {locations[-1]} created."

    def get_customer(self, email: str, name: str="") -> Customer:
        for customer in self._customers: # Search by email for existing customer
            if customer.email == email:
                return customer

        # If customer doesn't exist, create a new one
        customer = Customer(name, email)
        self._customers.append(customer)
        return customer

#
# Saving app state to file
#

    def dump_init(self, state: dict[str:dict]):
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
            state["packages"][package._package_id] = { # TODO: Package doesn't have unique ID
                "weight": package.weight,
                "pickup": package._pickup_loc, # TODO: Package doesn't have locations getters
                "dropoff": package._dropoff_loc,
                "customer_id": 0, # TODO: Package doesn't have customer ID
                "status": package.status,
                "current_loc": package._current_loc, # TODO: Package doesn't have current location getter
                "date_creation": package._date_creation # TODO: Package doesn't have creation date getter
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