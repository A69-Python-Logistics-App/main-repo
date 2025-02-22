from commands.base.base_command import BaseCommand
from models.helpers.validation_helpers import parse_to_int
from models.user import User


class FastForwardCommand(BaseCommand):

    PERMISSION = User.MANAGER
    PARAMS = 2
    USAGE = "fastforward {num} {type}"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self):
        number, type = self.params

        # Number error checking
        number = parse_to_int(number)
        
        if number < 0:
            raise ValueError("Number for hours/days must be positive.")
        
        # Type error checking
        type = type.lower()
        if type not in ["hour", "hours", "day", "days"]:
            raise ValueError("Type must be either day/s or hour/s.")
        
        # Fast forward error checking - returns none if not executed properly in appdata
        output = self.app_data.fast_forward(number, type)
        if output == None:
            raise ValueError("Fast forward general error.")
        return output

       