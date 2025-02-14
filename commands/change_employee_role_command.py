from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.user import User
from tests.create_package_command_test import valid_params


class ChangeEmployeeRoleCommand(BaseCommand):

    PERMISSION = User.ADMIN

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(2)
        # changeemployeerole {employee.email} {role}

    def execute(self):
        customer, role = self.params

        customer = self.app_data.find_customer_by_email(email)

        if not customer:
            raise ValueError(f"Customer with email {email} not found!")

        return self.app_data.update_customer(customer, new_first_name, new_last_name)