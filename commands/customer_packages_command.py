from commands.base.base_command import BaseCommand
from models.user import User


class CustomerPackagesCommand(BaseCommand):

    PERMISSION = User.USER
    PARAMS = 1
    USAGE = "customerpackages {email}"

    def __init__(self, params, app_data):
        super().__init__(params, app_data)

    def execute(self):
        email, = self.params
        customer = self.app_data.find_customer_by_email(email)

        if not customer:
            raise ValueError(f"Customer with email {email} not found!")
        if len(customer.package_ids) == 0:
            raise ValueError(f"Customer '{customer.first_name}' has no packages!")

        output = f"Customer '{customer.first_name}' packages:"
        for package in self.app_data.packages:
            if customer.find_package_by_id(package.id):
                output += f"\n Id: {package.id} | Location: {package.current_location} | Status: {package.status}"
        return output