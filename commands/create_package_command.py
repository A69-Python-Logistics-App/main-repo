
from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.location import Location


class CreatePackageCommand(BaseCommand):

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(4)

    def execute(self):
        # Unpacking values from params
        weight, pickup, dropoff, customer_email = self.params

        # Trying to parse weight into an integer value
        try:
            weight = int(weight)
        except:
            raise ValueError(f"Invalid number ({weight}) provided for weight!")

        # Making sure the pickup and dropoff locations are valid
        Location.validate_locations(pickup, dropoff)

        # Trying to find existing customer or raise ValueError
        customer = self.app_data.find_customer_by_email(customer_email)
        if not customer:
            raise ValueError(f"Customer with email {customer_email} not found!")

        # returning the result of create_package execution
        return self.app_data.create_package(weight, pickup, dropoff, customer.id)