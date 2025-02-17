from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User


class CreateEmployeeCommand(BaseCommand):

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.PERMISSION = self.app_data.current_employee.role
        self.validate_params(3)
        # createemployee {username} {password} {role}

    def execute(self):

        # Unpack
        username, password, role = self.params

        # Check if username exists
        if self.app_data.find_employee_by_username(username):
            raise ValueError(f"Employee with username '{username}' already exists!")
        
        # Check if role exists
        if not User.role_exists(role):
            raise ValueError(f"Role '{role}' is invalid!")

        if role in [User.ADMIN, User.SUPERVISOR, User.MANAGER, User.USER] and self.employee.can_execute(User.ADMIN):
            employee = self.app_data.create_employee(username, password, role)

        elif role in [User.SUPERVISOR, User.MANAGER, User.USER] and self.employee.can_execute(User.SUPERVISOR):
            employee = self.app_data.create_employee(username, password, role)

        elif role in [User.MANAGER, User.USER] and self.employee.can_execute(User.MANAGER):
            employee = self.app_data.create_employee(username, password, role)

        elif role in [User.USER] and self.employee.can_execute(User.USER):
            employee = self.app_data.create_employee(username, password, role)

        else:
            raise ValueError(f"You do not have permission to create an employee with role '{role}'!")

        return f"Employee with username '{employee.username}' and role {employee.role.upper()} created."