from datetime import datetime

from core.command_factory import CommandFactory


class Engine:
    def __init__(self, cmdf: CommandFactory):
        # read state
        self._command_factory = cmdf
        self._log = []

    def start(self):

        print("=" * 10 + " Welcome to Logistics App " + "=" * 10)
        while True:
            cmd = input("> ")

            if cmd == "exit":
                # write state
                self.stop()
                break

            try:
                command = self._command_factory.create(cmd)
                log_entry = command.execute()
            except Exception as e:
                log_entry = e.args[0]

            print(log_entry)
            self._log.append(f"[{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}] " + log_entry)

    def stop(self):
        print("\n".join(self._log))
        print("=" * 10 + " Goodbye " + "=" * 10)