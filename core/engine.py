from datetime import datetime

from core.command_factory import CommandFactory
from models.helpers.validation_helpers import get_login_info


class Engine:

    def __init__(self, cmdf: CommandFactory):
        # read state
        # TODO: implement file storage for app state during exit/init
        self._command_factory = cmdf

        # Ask to load from history
        if input("system > Load from local history? (y for yes): ").lower() == "y":
            self._load_state()

        # Engine loaded
        self.log("Program started")

    def start(self):

        print("=" * 10 + " Welcome to Logistics App " + "=" * 10)
        while True:

            # Ensure employee has logged in
            if not self._command_factory.app_data.login():
                self.stop()

            try:
                cmd = input(f"{self._command_factory.app_data.current_employee.role} > ")

                if cmd == "exit":
                    # write state ??
                    self.stop()
                    break

                command = self._command_factory.create(cmd)
                log_entry = command.execute()
            except SystemExit:
                self.log("Program ending")
                self.stop()
                break
            except Exception as e:
                log_entry = e.args[0]

            print(log_entry) # printing to console before exit will be required for finding the best route
            self.log(log_entry)

    def stop(self):
        self._command_factory.app_data.dump_state_to_file()
        print("=" * 10 + " Goodbye " + "=" * 10)
        print("\n>> ".join(["> Event log: "] + self._command_factory.app_data.log))

    def log(self, entry: str):
        self._command_factory.app_data.log_entry(entry)

    def _load_state(self):
        # TODO: Maybe move this in application_data.py?
        self.log("Attempting to load data from history...")
        dump = self._command_factory.app_data.dump_state_to_app()
        self.log(dump)
