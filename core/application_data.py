from models.Package import Package


class ApplicationData:

    def __init__(self):
        # TODO: Implement app data collections
        pass

    def create_package(self, weight, pickup, dropoff, customer):
        package = Package(weight, pickup, dropoff, customer)
        # TODO: Implement new package storage
        return f"Package #{package.id} created."