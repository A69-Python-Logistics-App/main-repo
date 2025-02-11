from models.Package import Package


class ApplicationData:

    def __init__(self):
        # TODO: Implement collections
        self._routes = []
        self._customers = []
        self._packages = []
        self._locations = []

    def create_package(self, weight, pickup, dropoff, customer):
        package = Package(weight, pickup, dropoff, customer)
        # TODO: Implement new package storage
        return f"Package #{package.id} created."