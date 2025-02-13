import string

from pandas.core.computation.expressions import evaluate


class User:

    # Permissions
    ROLES = {"WRITE": "admin", "READ_ONLY": "user"}

    READ_ONLY = [ # Add all read-only commands
        "Routes",
        "CustomerPackage",
        "Logout"

    ]

    WRITE = READ_ONLY + [
        "CreateCustomer",
        "CreatePackage",
        "CreateRoute",
        "RemoveCustomer",
        "RemovePackage",
        "RemoveRoute",
        "UpdateCustomer",
        "Reset"
    ]

    USERNAMES = []

    def __init__(self, username: str, password: str, role: str=ROLES["READ_ONLY"]):
        if len(username) < 4 or len(username) > 16:
            raise ValueError(f"Invalid username provided ({len(username)} characters long, expected 4-16)!")
        if not set(username).issubset(set(string.ascii_letters + string.digits + "_")):
            raise ValueError(f"Invalid characters in username. Use only characters, digits and underscore (_).")
        if username in self.USERNAMES:
            raise ValueError(f"Employee with username {username} already exists.")
        self._role = role
        self._username = username
        self.password = password
        self.USERNAMES.append(username)

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        if len(password) < 6 or len(password) > 18:
            raise ValueError(f"Invalid password provided ({len(password)} characters long, expected 6-18)!")
        if not set(password).issubset(set(string.ascii_letters + string.digits + "_-*@#$")):
            raise ValueError(f"Invalid characters in password. Use only characters, digits and [_, -, *, @, #, $]!")
        self._password = password

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, role):
        if role not in self.ROLES.values():
            raise ValueError(f"Invalid employee role: {role}")
        if role == self._role:
            raise ValueError(f"Employee role is already set to {role}")
        self._role = role

    def can_execute(self, command: str) -> bool:
        if self.role == self.ROLES["WRITE"]:
            return True
        return command in self.READ_ONLY

### TESTING

    def test(self, test):
        return getattr(self.__class__, test)

# user = User("admin", "password")
# print(user.test("READ_ONLY"))