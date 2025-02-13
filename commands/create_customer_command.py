from commands.base.base_command import BaseCommand
from models.user import User


class CreateCustomerCommand(BaseCommand):

    PERMISSION = User.USER

    def __init__(self, params, app_data):
        super().__init__(params, app_data)
        self.validate_params(3)

    def execute(self):
        # Unpack values
        first_name, last_name, email = self.params
        # Try to find existing customer or create a new one
        customer = self.app_data.find_customer_by_email(email)
        if customer:
            raise ValueError("Customer already exists!")
        customer = self.app_data.create_customer(first_name, last_name, email)
        return f"Customer with id {customer.id} created."