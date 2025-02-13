from datetime import datetime

from core.command_factory import CommandFactory


class Engine:

    def __init__(self, cmdf: CommandFactory):
        # read state
        # TODO: implement file storage for app state during exit/init
        self._command_factory = cmdf
        self._log = []
        self._load_state()

        # Engine loaded
        self.log("Program started")

    def start(self):

        print("=" * 10 + " Welcome to Logistics App " + "=" * 10)
        while True:
            cmd = input("> ")

            if cmd == "exit":
                # write state ??
                self.stop()
                break

            try:
                command = self._command_factory.create(cmd)
                log_entry = command.execute()
            except SystemExit:
                self.log("Application Data wiped out. Restart program.")
                self.stop()
                break
            except Exception as e:
                log_entry = e.args[0]

            print(log_entry) # printing to console before exit will be required for finding the best route
            self.log(log_entry)

    def stop(self):
        self.log("Program ended")
        self._command_factory.app_data.dump_state_to_file(self._log)
        print("=" * 10 + " Goodbye " + "=" * 10)
        print("\n>> ".join(["> Event log: "] + self._log))

    def log(self, entry: str):
        self._log.append(f"{self.fdate()} {entry}")

    def fdate(self) -> str:
        employee = self._command_factory.app_data.current_employee
        login = employee.username if employee else "None"
        return f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][{login}]:"

    def _load_state(self):
        # TODO: Maybe move this in application_data.py?
        dump = self._command_factory.app_data.dump_state_to_app()
        self.log(dump)