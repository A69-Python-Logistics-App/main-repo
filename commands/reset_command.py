from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData


class ResetCommand(BaseCommand):

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(0)
        # TODO: Verify employee credentials

    def execute(self):
        self.app_data.reset_app()