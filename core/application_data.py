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