from commands.base.base_command import BaseCommand

class CustomerPackagesCommand(BaseCommand):
    def __init__(self, params, app_data):
        super().__init__(params, app_data)
        self.validate_params(1)

    def execute(self):
        email = ''.join(self.params)
        customer = self.app_data.find_customer_by_email(email)

        if not customer:
            raise ValueError(f"Customer with email {email} not found!")
        if len(customer.packages) == 0:
            raise ValueError(f"Customer '{customer.first_name}' has no packages!")

        output = f"Customer '{customer.first_name}' packages:"
        for package in customer.packages:
            output += f"\n Id: {package.id} | Location: {package.current_location} | Status: {package.status}"
        return output