from commands.base.base_command import BaseCommand
from models.user import User


class UpdateCustomerCommand(BaseCommand):

    PERMISSION = User.USER

    def __init__(self, params, app_data):
        super().__init__(params, app_data)
        self.validate_params(3)
        # updatecustomer {email} {new_first_name} {new_last_name}

    def execute(self) -> str:
        email, new_first_name, new_last_name = self.params

        customer = self.app_data.find_customer_by_email(email)

        if not customer:
            raise ValueError(f"Customer with email {email} not found!")

        return self.app_data.update_customer(customer, new_first_name, new_last_name)