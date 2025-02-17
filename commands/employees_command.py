from commands.base.base_command import BaseCommand
from models.user import User


class EmployeesCommand(BaseCommand):

    PERMISSION = User.SUPERVISOR
    PARAMS = 0
    USAGE = "employees command takes no parameters"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self):
        output = []
        for employee in self.app_data.employees:
            output.append(str(employee))

        if len(output) == 0:
            return "There are no employees in the system."

        return "system > Employees: \n" + "\n".join(output)
