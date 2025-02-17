from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User


class RemoveEmployeeCommand(BaseCommand):

    PERMISSION = User.ADMIN
    PARAMS = 1
    USAGE = "removeemployee {username}"

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):

        username, = self.params

        # Check if username exists
        if not self.app_data.find_employee_by_username(username):
            raise ValueError(f"Employee with username '{username}' doesn't exist!")
        
        # Check if the employee is the current employee
        if self.app_data.current_employee.username == username:
            raise ValueError(f"Cannot remove yourself!")
        
        return self.app_data.remove_employee(username)