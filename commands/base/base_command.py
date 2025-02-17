from core.application_data import ApplicationData
from models.user import User


class BaseCommand:

    PERMISSION = User.USER
    PARAMS = -1
    USAGE = "Unspecified, must override in command class"
    SPECIAL_CASE  = False

    def __init__(self, params: list[str], app_data: ApplicationData):
        self._params: list[str] = params
        self._app_data: ApplicationData = app_data

        # Validates if the parameters are correct, else prints message for the proper command use
        # Note: self.PARAMS must be overriden by child command or error will be raised
        self.validate_params()

        # Validate if self.PERMISSION permits for execution of this command, else throws an error
        # Note: self.PERMISSION must be overriden by child command class if necessary
        self.require_permission()

    @property
    def params(self) -> tuple[str, ...]:
        return tuple(self._params)

    @property
    def app_data(self)-> ApplicationData:
        return self._app_data

    @property
    def employee(self) -> User:
        return self._app_data.current_employee

    def validate_params(self) -> None:
        if len(self._params) != self.PARAMS and not self.SPECIAL_CASE:
            raise ValueError(f"Expected {self.PARAMS} parameters, got {len(self._params)} instead.{"\n - Usage: " + self.USAGE or ""}")

    def require_permission(self) -> None:
        if not self.employee.can_execute(self.PERMISSION):
            raise ValueError(f"You do not have permission to use this command!")

    def execute(self) -> str:
        raise NotImplementedError("BaseCommand requires child commands to override execute method.")