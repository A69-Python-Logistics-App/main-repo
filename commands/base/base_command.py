from core.application_data import ApplicationData
from models.user import User


class BaseCommand:

    PERMISSION = User.USER

    def __init__(self, params: list[str], app_data: ApplicationData):
        self._params: list[str] = params
        self._app_data: ApplicationData = app_data
        self._app_data.update_state()
        self.require_permission()

    @property
    def params(self) -> tuple[str, ...]:
        return tuple(self._params)

    @property
    def app_data(self)-> ApplicationData:
        return self._app_data

    @property
    def employee(self):
        return self._app_data.current_employee

    def validate_params(self, count: int) -> None:
        if len(self._params) != count:
            raise ValueError(f"Expected {count} parameters, got {len(self._params)} instead")

    def require_permission(self):
        if not self.employee.can_execute(self.PERMISSION):
            raise ValueError(f"You do not have permission to use this command!")

    def execute(self) -> str:
        raise NotImplementedError