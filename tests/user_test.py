import unittest
from models.user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        # Clear USERNAMES before each test
        User.USERNAMES.clear()

    def test_valid_user_creation(self):
        user = User("validUser", "validPass1", User.USER)
        self.assertEqual(user.username, "validUser")
        self.assertEqual(user.password, "validPass1")
        self.assertEqual(user.role, User.USER)

    def test_invalid_username_too_short(self):
        with self.assertRaises(ValueError):
            User("abc", "validPass1", User.USER)

    def test_invalid_username_too_long(self):
        with self.assertRaises(ValueError):
            User("a" * 17, "validPass1", User.USER)

    def test_invalid_username_characters(self):
        with self.assertRaises(ValueError):
            User("invalid@name", "validPass1", User.USER)

    def test_duplicate_username(self):
        User("uniqueUser", "validPass1", User.USER)
        with self.assertRaises(ValueError):
            User("uniqueUser", "validPass2", User.USER)

    def test_invalid_password_too_short(self):
        with self.assertRaises(ValueError):
            User("validUser", "short", User.USER)

    def test_invalid_password_too_long(self):
        with self.assertRaises(ValueError):
            User("validUser", "a" * 19, User.USER)

    def test_invalid_password_characters(self):
        with self.assertRaises(ValueError):
            User("validUser", "invalid^pass", User.USER)

    def test_role_validation(self):
        with self.assertRaises(ValueError):
            User("validUser", "validPass1", "invalidRole")

    def test_can_execute(self):
        user = User("validUser", "validPass1", User.USER)
        self.assertTrue(user.can_execute(User.USER))
        self.assertFalse(user.can_execute(User.MANAGER))

        manager = User("managerUser", "validPass1", User.MANAGER)
        self.assertTrue(manager.can_execute(User.USER))
        self.assertTrue(manager.can_execute(User.MANAGER))
        self.assertFalse(manager.can_execute(User.SUPERVISOR))

        supervisor = User("supervisorUser", "validPass1", User.SUPERVISOR)
        self.assertTrue(supervisor.can_execute(User.USER))
        self.assertTrue(supervisor.can_execute(User.MANAGER))
        self.assertTrue(supervisor.can_execute(User.SUPERVISOR))
        self.assertFalse(supervisor.can_execute(User.ADMIN))

        admin = User("adminUser", "validPass1", User.ADMIN)
        self.assertTrue(admin.can_execute(User.USER))
        self.assertTrue(admin.can_execute(User.MANAGER))
        self.assertTrue(admin.can_execute(User.SUPERVISOR))
        self.assertTrue(admin.can_execute(User.ADMIN))