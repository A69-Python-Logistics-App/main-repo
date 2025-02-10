from core.command_factory import CommandFactory


class Engine:
    def __init__(self, cmdf: CommandFactory):
        # read state
        self._command_factory = cmdf

    def start(self):
        print("=" * 10 + " Welcome to Logistics App " + "=" * 10)
        while True:
            cmd = input("> ")

            if cmd == "exit":
                # write state
                self.stop()
                break

            try:
                self._command_factory.create(cmd) # TODO: add execute method
            except Exception as e:
                print(e.args[0])

    def stop(self):
        print("=" * 10 + " Goodbye " + "=" * 10)