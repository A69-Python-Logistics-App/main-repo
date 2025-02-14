
class Status:

    STATUSES = {
        0: "Collected",
        1: "On Route",
        2: "Delivered"}

    def __init__(self):
        """
        Package status. Can be: "Collected" (default), "On Route", "Delivered".
        """
        self._sts = 0 # 'Collected' by def
        self._value = Status.STATUSES[self._sts] # 'Collected' by def

    @property
    def current(self):
        """
        Return current package status.
        """
        return self._value

    def _advance_status(self):
        self._sts += 1

    def advance_status(self):
        """
        Advance package status.
        """
        if self._sts >= 2:
            raise ValueError(f"Cannot advance product status, limit already reached. Final: {self.current}.")
        else:
            self._advance_status()
