
from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.helpers.validation_helpers import parse_to_int
from models.location import Location
from models.user import User


class CreatePackageCommand(BaseCommand):

    PERMISSION = User.USER
    PARAMS = 4
    USAGE = "createpackage {weight_in_kg} {pickup} {dropoff} {customer_email}"

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        # Unpacking values from params
        weight, pickup, dropoff, customer_email = self.params

        # Trying to parse weight into an integer value
        weight = parse_to_int(weight)

        # Making sure the pickup and dropoff locations are valid
        Location.validate_locations([pickup, dropoff])

        # Trying to find existing customer or raise ValueError
        customer = self.app_data.find_customer_by_email(customer_email)
        if not customer:
            raise ValueError(f"Customer with email {customer_email} not found!")

        # returning the result of create_package execution
        p = self.app_data.create_package(weight, pickup, dropoff, customer.id)
        return f"Package #{p.id} created and added to customer #{p.customer_id}."