from commands.base.base_command import BaseCommand
from models.user import User


class RemoveCustomerCommand(BaseCommand):

    PERMISSION = User.SUPERVISOR

    def __init__(self, params, app_data):
        super().__init__(params, app_data)
        self.validate_params(1)
        # removecustomer {email}

    def execute(self) -> str:
        email = self.params[0]
        customer = self.app_data.find_customer_by_email(email)

        if not customer:
            raise ValueError(f"Customer with email {email} not found!")

        return self.app_data.remove_customer(customer)