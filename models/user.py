import string


class User:

    # Permissions
    ROLES = {"WRITE": "admin", "READ_ONLY": "user"}

    READ_ONLY = [ # Add all read-only commands
        "routes"
    ]

    ADMIN = READ_ONLY + [ # Add all write commands
        "create_customer", "create_package", "create_route"
    ]

    def __init__(self, username: str, password: str, role: str=ROLES["READ_ONLY"]):
        if len(username) < 4 or len(username) > 16:
            raise ValueError(f"Invalid username provided ({len(username)}), expected 4-16 characters!")
        if not set(username).issubset(set(string.ascii_letters + string.digits + "_")):
            raise ValueError(f"Invalid characters in username. Use only characters, digits and underscore (_).")
        self._role = role
        self._username = username
        self.password = password

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
            # invalid characters in password
            raise ValueError(f"Invalid characters in password. Use only characters, digits and [_, -, *, @, #, $]!")
        self._password = password

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, role):
        if role not in self.ROLES.values():
            raise ValueError(f"Invalid employee role: {role}")
        self._role = role

    def can_execute(self, command: str) -> bool:
        if self.role == self.ROLES["all"]:
            return True
        return command in self.ROLES[self.role]