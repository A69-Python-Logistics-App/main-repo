from datetime import datetime

from models.package import Package
from models.route import Route


class ApplicationData:

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

    def create_route(self, date: datetime, *locations: [str]) -> str:
        # TODO: fix implementation with the correct location validation
        try:
            route = Route(["SYD", "MEL"], date) # TODO: placeholder values
        except Exception as e:
            return e.args[0]

        self._routes.append(route)
        return f"Route #{"route.id"} from {locations[0]} to {locations[-1]} created."