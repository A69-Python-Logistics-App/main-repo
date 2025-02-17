from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User


class RoutesCommand(BaseCommand):

    PERMISSION = User.USER
    PARAMS = 0
    USAGE = "routes command takes no parameters"

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        routes = self.app_data.routes


        output = []
        # Check if there are any routes
        if len(routes) == 0:
            output.append("There are no routes in the system.")
        else:
            # Print routes
            for route in self.app_data.routes:
                output.append(str(route))

        # returning the output joined with a new line
        return "\n".join(output)