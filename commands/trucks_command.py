from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User


class TrucksCommand(BaseCommand):

    PERMISSION = User.USER
    PARAMS = 0
    USAGE = "trucks command takes no parameters"

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        trucks = self.app_data.truck_park.trucks


        output = []
        # Print trucks
        for truck in trucks:
            output.append(str(truck))

        # returning the output joined with a new line
        return "\n".join(output)