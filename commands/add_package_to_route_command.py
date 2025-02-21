from commands.base.base_command import BaseCommand
from models.user import User
from models.helpers.validation_helpers import parse_to_int

class AddPackageToRouteCommand(BaseCommand):

    PERMISSION = User.MANAGER
    PARAMS = 2
    USAGE = "addpackagetoroute {package_id} {route_id}"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self) -> str:
        package_id = parse_to_int(self.params[0])
        route_id = parse_to_int(self.params[1])

        package = self.app_data.find_package_by_id(package_id)
        if not package:
            raise ValueError(f"Package with id {package_id} not found!")

        route = self.app_data.find_route_by_id(route_id)
        if not route:
            raise ValueError(f"Route with id {route_id} not found!")

        self.app_data.assign_package_to_route(package_id, route_id)
        return f"Package #{package_id} assigned to route #{route_id}."