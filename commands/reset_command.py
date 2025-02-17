from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User


class ResetCommand(BaseCommand):

    PERMISSION = User.ADMIN
    PARAMS = 0
    USAGE = "system_reset command takes no parameters"

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        self.app_data.reset_app()