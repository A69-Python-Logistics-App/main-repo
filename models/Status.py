
class Status():

    """
    Package status. Can be: "Collected", "On Route", "Delivered".
    """

    Status_Types = {0: "Collected", 1: "On Route", 2: "Delivered"}

    def __init__(self):
        self.value = Status.Status_Types[0] # value by default
        self.idx = 0 # used for advance status

    @property
    def current(self):
        """
        Return current package status.
        """
        return self.value
    
    def advance_status(self):
        """
        Advance package status.
        """
        self.idx += 1
        if self.idx not in [1, 2]:
            raise ValueError(f"Invalid status (index = {self.idx})!")
        self.value = Status.Status_Types[self.idx]