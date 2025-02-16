from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User


class CreateEmployeeCommand(BaseCommand):

    PERMISSION = User.MANAGER

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(3)
        # createemployee {username} {password} {role}

    def execute(self):
        # Unpack
        username, password, role = self.params
        role = role.lower()
        # Check if username exists
        if self.app_data.find_employee_by_username(username):
            raise ValueError(f"Employee with username '{username}' already exists!")
        # Check if role exists
        if not User.role_exists(role):
            raise ValueError(f"Role '{role}' is invalid!")
        
        if role == User.USER:
            employee = self.app_data.create_user(username, password, role)
            return f"Employee with username '{employee.username}' and role {employee.role.upper()} created."
        
        if role == User.MANAGER:
            employee = self.app_data.create_manager(username, password, role)
            return f"Employee with username '{employee.username}' and role {employee.role.upper()} created."

        if role == User.SUPERVISOR:
            employee = self.app_data.create_supervisor(username, password, role)
            return f"Employee with username '{employee.username}' and role {employee.role.upper()} created."
        
        if role == User.ADMIN:
            employee = self.app_data.create_admin(username, password, role)
            return f"Employee with username '{employee.username}' and role {employee.role.upper()} created."
        
        