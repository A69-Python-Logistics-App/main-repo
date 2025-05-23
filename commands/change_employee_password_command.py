from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User

class ChangeEmployeePasswordCommand(BaseCommand):

    PERMISSION = User.ADMIN
    PARAMS = 2
    USAGE = "changeemployeepassword {employee} {new password}"

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        employee, new_password = self.params

        # Check if employee exists
        if not self.app_data.find_employee_by_username(employee):
            raise ValueError(f"Employee '{employee}' does not exist!")
        
        return self.app_data.update_employee_password(employee, new_password)
