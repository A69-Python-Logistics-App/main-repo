from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User
from tests.create_package_command_test import valid_params


class ChangeEmployeeRoleCommand(BaseCommand):

    PERMISSION = User.SUPERVISOR

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(2)
        # changeemployeerole {employee} {role}

    def execute(self):
        employee, role = self.params

        if employee == self.employee.username:
            raise ValueError("You cannot change your own role!")

        if not self.employee.can_execute(User.ADMIN):
            if role not in (User.MANAGER, User.USER):
                raise ValueError("You do not have permission to apply this change.")

        return self.app_data.update_employee_role(employee, role)