from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.helpers.validation_helpers import parse_to_int
from models.user import User


class RemoveRouteCommand(BaseCommand):

    PERMISSION = User.MANAGER

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(1)
        # removeroute {route_id}

    def execute(self) -> str:
        id_number = parse_to_int(self.params[0])

        route = self.app_data.find_route_by_id(id_number)
        if not route:
            raise ValueError(f"Route with id {id_number} not found!")

        return self.app_data.remove_route(route)