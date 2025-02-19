from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.route import Route
from models.package import Package
from models.helpers.validation_helpers import parse_to_int


class AddPackageCommand(BaseCommand):

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self):
        pickup_location = self.params[0]
        dropoff_location = self.params[1]
        weight = parse_to_int(self.params[2])
        package = Package(pickup_location=pickup_location, dropoff_location=dropoff_location, weight=weight)

        try:
            route = self.app_data.find_route_by_locations(pickup_location, dropoff_location)
            self.app_data.assign_package_to_route(package, route.route_id)
            return f"Package added successfully"
        except ValueError as e:
            return f"Error {e}"

       