from datetime import datetime

from core.command_factory import CommandFactory


class Engine:
    def __init__(self, cmdf: CommandFactory):
        # read state
        # TODO: implement file storage for app state during exit/init
        self._command_factory = cmdf
        self._log = [f"[{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}]: System started"]

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
            except Exception as e:
                log_entry = e.args[0]

            print(log_entry) # printing to console before exit will be required for finding the best route
            self._log.append(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] " + log_entry)

    def stop(self):
        self._command_factory.app_data.save_state_to_history(self._log)
        print("Event log: ")
        print("\n".join(self._log))
        print("=" * 10 + " Goodbye " + "=" * 10)