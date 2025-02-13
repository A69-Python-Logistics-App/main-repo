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
        pass