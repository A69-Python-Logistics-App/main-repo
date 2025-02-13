from datetime import datetime

from core.command_factory import CommandFactory
from models.helpers.validation_helpers import get_login_info


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

            try:
                # Make sure there is always an employee logged in
                self.employee_login()

                cmd = input("> ")

                if cmd == "exit":
                    # write state ??
                    raise SystemExit

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
        self.log("Attempting to load data from history...")
        dump = self._command_factory.app_data.dump_state_to_app()
        self.log(dump)

    def employee_login(self):
        app_data = self._command_factory.app_data
        while not app_data.current_employee:
            # repeat until the user logs in an employee account
            # check if there are employee accounts:
            while not len(app_data.employees):
                try:
                    # ask user to make an employee account until it's valid
                    username, password = get_login_info("Create admin")
                    app_data.create_employee(username, password, "admin", True)
                    self.log(f"Employee {app_data.current_employee.username} created and logged in")
                except ValueError as e:
                    print(e.args[0])
                    continue

            if app_data.current_employee:
                break # making sure we break if employee is created (auto log in)

            # There is at least one employee account
            try:
                username, password = get_login_info("Login")
                app_data.employee_login(username, password)
                self.log(f"Employee {username} logged in")
            except ValueError as e:
                print(e.args[0])
                continue

        # user is logged in