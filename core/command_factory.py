from commands.base.base_command import BaseCommand
from commands.create_package_command import CreatePackageCommand
from core.application_data import ApplicationData


class CommandFactory:
    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data

    def create(self, command: str) -> BaseCommand:

        cmd, *params = command.split()

        match cmd.lower():
            case "createpackage":
                return CreatePackageCommand(params, self._app_data)
            case _:
                raise ValueError(f"Unknown command: {cmd}")