from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User

class ChangeEmployeeRoleCommand(BaseCommand):

    # This will make ensure only supervisors can run the command
    PERMISSION = User.SUPERVISOR
    PARAMS = 2
    USAGE = "changeemployeerole {employee} {role}"

    # Missing __init__ which validates params and permission
    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        employee, role = self.params
        role = role.lower()

        # Check if user is trying to change own role
        if employee == self.app_data.current_employee.username:
            raise ValueError("You cannot change your own role!")

        # Check if role exists
        if not User.role_exists(role):
            raise ValueError(f"Role '{role}' is invalid!")
        
        # Check if employee exists
        if not self.app_data.find_employee_by_username(employee):
            raise ValueError(f"Employee '{employee}' does not exist!")

        # I think only admins and supervisors should be able to change roles. Modify this if needed.
        if role in [User.ADMIN, User.SUPERVISOR, User.MANAGER, User.USER] and self.employee.can_execute(User.ADMIN):
            return self.app_data.update_employee_role(employee, role)

        elif role in [User.MANAGER, User.USER] and self.employee.can_execute(User.SUPERVISOR):
            return self.app_data.update_employee_role(employee, role)

        else:
            raise ValueError(f"You do not have permission to change employee '{employee}' role to {role.upper()}!")