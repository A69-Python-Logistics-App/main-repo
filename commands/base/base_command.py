from core.application_data import ApplicationData


class BaseCommand:
    def __init__(self, params: list[str], app_data: ApplicationData, login: bool=False):
        self._params: list[str] = params
        self._app_data: ApplicationData = app_data
        if login:
            self.require_login()

    @property
    def params(self) -> tuple[str, ...]:
        return tuple(self._params)

    @property
    def app_data(self)-> ApplicationData:
        return self._app_data

    def validate_params(self, count: int) -> None:
        if len(self._params) != count:
            raise ValueError(f"Expected {count} parameters, got {len(self._params)} instead")

    def require_login(self):
        if not self._app_data.employee:
            raise ValueError("You must be logged in to use this command!")

    def require_permission(self):
        cmd = self.__class__.__name__.replace("Command", "")
        if not self._app_data.employee.can_execute(cmd.lower()):
            raise ValueError(f"You do not have permission to use {cmd} command!")

    def execute(self) -> str:
        raise NotImplementedError