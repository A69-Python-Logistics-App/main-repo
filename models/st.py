
class Status():

    """
    Package status. Can be: "Collected", "On Route", "Delivered".
    """

    _class_status_types = {0: "Collected", 1: "On Route", 2: "Delivered"}

    def __init__(self):
        self._value = Status._class_status_types[0] # Collected value by default
        self._idx = 0 # used for advance status

    @property
    def current(self):
        """
        Return current package status.
        """
        return self._value
    
    def advance_status(self):
        """
        Advance package status.
        """
        self._idx += 1
        if self._idx not in [1, 2]:
            # raise ValueError(f"Invalid status (index = {self._idx})!")
            self._value = Status._class_status_types[2]
        else:
            self._value = Status._class_status_types[self._idx]
    