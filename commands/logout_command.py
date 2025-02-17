from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User


class LogoutCommand(BaseCommand):

    PERMISSION = User.USER

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(0)

    def execute(self):
        employee = self.app_data.current_employee.username
        self.app_data.logout()
        return f"User {employee} successfully logged out!"
