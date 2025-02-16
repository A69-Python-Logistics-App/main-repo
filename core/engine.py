
from core.command_factory import CommandFactory
from models.helpers import state


class Engine:

    def __init__(self, cmdf: CommandFactory):
        self._command_factory = cmdf

        # Ask to load from history
        self._init_history()

    @property
    def app_data(self):
        return self.app_data

    def start(self):

        # Engine loaded
        self.log("Program started")

        print("=" * 10 + " Welcome to Logistics App " + "=" * 10)
        cmd = ""

        while True:

            # Ensure employee has logged in
            while not self.app_data.current_employee:
                self.app_data.login()

            try:
                if cmd == "exit":
                    self.stop()
                    break

                cmd = input(f"{self.app_data.current_employee.role} > ")

                command = self._command_factory.create(cmd)
                if command:
                    log_entry = command.execute()
                else:
                    continue
            except Exception as e:
                # print(traceback.print_tb(e.__traceback__))
                log_entry = e.args[0]
                # exit()

            print(log_entry) # printing to console before exit will be required for finding the best route
            self.log(log_entry)

    def stop(self):
        self.log("Program exited.")
        state.dump_to_file(self.app_data)
        print("=" * 10 + " Goodbye " + "=" * 10)
        print("\n>> ".join(["> Event log: "] + self.app_data.log))

    def log(self, entry: str):
        self.app_data.log_entry(entry)

    def _load_state(self):
        # TODO: Maybe move this in application_data.py?
        self.log("Attempting to load data from history...")
        #dump = self.app_data.dump_state_to_app()
        dump = state.dump_to_app(self.app_data)
        self.log(dump)

    def _init_history(self):
        load = None
        while load not in ("y", "n"):
            load = input("system > Load application data from local storage? (y/n): ").lower()
            match load:
                case "y":
                    self._load_state()
                case "n":
                    break
                case _:
                    print("Invalid answer, expected y for yes or n for no.")
                    continue