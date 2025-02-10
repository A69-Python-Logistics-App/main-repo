from core.application_data import ApplicationData


class BaseCommand():
    def __init__(self, params: list[str], app_data: ApplicationData):
        self._params = params
        self._app_data = app_data

    @property
    def params(self):
        return self._params

    @property
    def app_data(self):
        return self._app_data

    def validate_params(self, count: int):
        if len(self._params) != count:
            raise ValueError(f"Expected {count} parameters, got {len(self._params)} instead")

    def execute(self):
        raise NotImplementedError