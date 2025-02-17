from ast import parse

from commands.base.base_command import BaseCommand
from models.helpers.validation_helpers import parse_to_int
from models.user import User


class RemovePackageCommand(BaseCommand):

    PERMISSION = User.USER
    PARAMS = 1
    USAGE = "removepackage {id}"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self) -> str:
        id_number = parse_to_int(self.params[0])

        package = self.app_data.find_package_by_id(id_number)
        if not package:
            raise ValueError(f"Package with id {id_number} not found!")

        return self.app_data.remove_package(package)