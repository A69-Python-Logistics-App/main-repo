from commands.base.base_command import BaseCommand
from core.application_data import ApplicationData
from models.Customer import Customer
from models.location import Location


class CreatePackageCommand(BaseCommand):

    def __init__(self, params: list[str], app_data: ApplicationData):
        super().__init__(params, app_data)
        self.validate_params(4)

    def execute(self):
        # Unpacking values from params
        weight, pickup, dropoff, customer = self.params

        # Trying to parse weight into an integer value
        try:
            weight = int(weight)
        except:
            raise ValueError(f"Invalid number ({weight}) provided for weight!")

        # Making sure the pickup and dropoff locations are valid
        Location.validate_locations(pickup, dropoff)

        # TODO: Validate customer exists or change customer implementation
        customer = Customer("test_name", "test_email@test.com")

        # returning the result of create_package execution
        return self.app_data.create_package(weight, pickup, dropoff, customer)