import string

from pandas.core.computation.expressions import evaluate


class User:

    # Permissions
    USER = "user"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

    USERNAMES = []

    def __init__(self, username: str, password: str, role: str):
        self.role = role
        self._username = self.validate_username(username)
        self.password = password
        self.USERNAMES.append(username)

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, username: str):
        self._username = self.validate_username(username)

    def validate_username(self, username: str) -> str:
        if len(username) < 4 or len(username) > 16:
            raise ValueError(f"Invalid username provided ({len(username)} characters long, expected 4-16)!")
        if not set(username).issubset(set(string.ascii_letters + string.digits + "_")):
            raise ValueError(f"Invalid characters in username. Use only characters, digits and underscore (_).")
        if username in self.USERNAMES:
            raise ValueError(f"Employee with username {username} already exists.")
        return username

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

    @classmethod
    def role_exists(cls, value) -> bool:
        return value in (cls.USER, cls.MANAGER, cls.SUPERVISOR, cls.ADMIN)

    def can_execute(self, role: str) -> bool:
        perms = {
            self.USER: [self.USER],
            self.MANAGER: [self.USER, self.MANAGER],
            self.SUPERVISOR: [self.USER, self.MANAGER, self.SUPERVISOR],
            self.ADMIN: [self.USER, self.MANAGER, self.SUPERVISOR, self.ADMIN]
        }
        if role not in perms[self.role]:
            return False
        return True

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, role):
        if not self.role_exists(role):
            raise ValueError(f"Invalid role {role}")
        self._role = role

    def __str__(self):
        max_username_length = max([len(usern) for usern in self.USERNAMES])
        return f"-> {self.username.ljust(max_username_length)} [{self.role.upper()}]"
