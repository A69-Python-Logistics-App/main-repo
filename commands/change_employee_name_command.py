from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User
from tests.create_package_command_test import valid_params


class ChangeEmployeeNameCommand(BaseCommand):

    PERMISSION = User.ADMIN
    PARAMS = 2
    USAGE = "changeemployeename {employee} {new username}"

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        employee, new_name = self.params

        # Check if employee exists
        if not self.app_data.find_employee_by_username(employee):
            raise ValueError(f"Employee '{employee}' does not exist!")
        
        # Check if new name exists
        if self.app_data.find_employee_by_username(new_name):
            raise ValueError(f"Name '{employee}' is already taken!")
        
        return self.app_data.update_employee_name(employee, new_name)

