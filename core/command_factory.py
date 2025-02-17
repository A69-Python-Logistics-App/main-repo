from commands.base.base_command import BaseCommand
from commands.create_employee_command import CreateEmployeeCommand
from commands.change_employee_role_command import ChangeEmployeeRoleCommand
from commands.create_customer_command import CreateCustomerCommand
from commands.create_package_command import CreatePackageCommand
from commands.create_route_command import CreateRouteCommand
from commands.customer_packages_command import CustomerPackagesCommand
from commands.employees_command import EmployeesCommand
from commands.logout_command import LogoutCommand
from commands.remove_customer_command import RemoveCustomerCommand
from commands.remove_package_command import RemovePackageCommand
from commands.remove_route_command import RemoveRouteCommand
from commands.reset_command import ResetCommand
from commands.routes_command import RoutesCommand
from commands.update_customer_command import UpdateCustomerCommand
from commands.change_employee_role_command import ChangeEmployeeRoleCommand
from commands.change_employee_name_command import ChangeEmployeeNameCommand
from commands.change_employee_password_command import ChangeEmployeePasswordCommand
from core.application_data import ApplicationData


class CommandFactory:
    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data

    @property
    def app_data(self):
        return self._app_data

    def create(self, command: str) -> BaseCommand | None:

        cmd, *params = command.split()

        match cmd.lower():
            # Employee commands
            case "createemployee":
                return CreateEmployeeCommand(params, self.app_data)
            case "changeemployeerole":
                return ChangeEmployeeRoleCommand(params, self.app_data)
            case "changeemployeename":
                return ChangeEmployeeNameCommand(params, self.app_data)
            case "changeemployeepassword":
                return ChangeEmployeePasswordCommand(params, self.app_data)
            case "employees":
                return EmployeesCommand(params, self.app_data)

            # Customer commands
            case "createcustomer":
                return CreateCustomerCommand(params, self.app_data)
            case "removecustomer":
                return RemoveCustomerCommand(params, self.app_data)
            case "updatecustomer":
                return UpdateCustomerCommand(params, self.app_data)
            case "customerpackages":
                return CustomerPackagesCommand(params, self.app_data)


            # Package commands
            case "createpackage":
                return CreatePackageCommand(params, self.app_data)
            case "removepackage":
                return RemovePackageCommand(params, self.app_data)

            # Route commands
            case "createroute":
                return CreateRouteCommand(params, self.app_data)
            case "removeroute":
                return RemoveRouteCommand(params, self.app_data)
            case "routes":
                return RoutesCommand(params, self.app_data)

            # System commands
            case "system_reset":
                return ResetCommand(params, self.app_data)
            case "logout":
                return LogoutCommand(params, self.app_data)
            case "exit":
                return None

            # Invalid command
            case _:
                raise ValueError(f"Unknown command: {cmd}")