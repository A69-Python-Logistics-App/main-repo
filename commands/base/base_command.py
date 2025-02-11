from core.application_data import ApplicationData


class BaseCommand:
    def __init__(self, params: list[str], app_data: ApplicationData):
        self._params: list[str] = params
        self._app_data: ApplicationData = app_data

    @property
    def params(self) -> tuple[str, ...]:
        return tuple(self._params)

    @property
    def app_data(self)-> ApplicationData:
        return self._app_data

    def validate_params(self, count: int) -> None:
        if len(self._params) != count:
            raise ValueError(f"Expected {count} parameters, got {len(self._params)} instead")

    def execute(self) -> str:
        raise NotImplementedError