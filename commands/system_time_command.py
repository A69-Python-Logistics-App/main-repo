from commands.base.base_command import BaseCommand
from models.user import User

class SystemTimeCommand(BaseCommand):

    PERMISSION = User.USER
    PARAMS = 0
    USAGE = "systemtime"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self):
        return f"Time is: {self.app_data.system_time}"