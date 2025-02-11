from core.application_data import ApplicationData


class CommandFactory:
    def __init__(self, app_data: ApplicationData):
        self._app_data = app_data

    def create(self, command: str) -> str:

        cmd, *params = command.split()

        match cmd:
            case _:
                raise ValueError(f"Unknown command: {cmd}")
            