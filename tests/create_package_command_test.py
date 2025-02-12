import unittest

from commands.create_package_command import CreatePackageCommand
from core.application_data import ApplicationData
from models.status import Status

# CUSTOMER
VALID_FIRST_NAME = "Siso"
VALID_LAST_NAME = "Test"
VALID_FULL_NAME = VALID_FIRST_NAME + " " + VALID_LAST_NAME
VALID_EMAIL = "siso@icloud.com"

# PACKAGE
VALID_WEIGHT = 100
VALID_PICKUP = "SYD"
VALID_DROPOFF = "MEL"

def invalid_params() -> list[str]:
    return [VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_FULL_NAME, VALID_EMAIL]

def valid_params() -> list[str]:
    return [VALID_WEIGHT, VALID_PICKUP, VALID_DROPOFF, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_EMAIL]

class Create_Package_Command_Should(unittest.TestCase):

    def test_raise_ValueError_when_InvalidParams(self):
        params = invalid_params()
        app_data = ApplicationData()

        with self.assertRaises(ValueError):
            CreatePackageCommand(params, app_data)

    def test_creates_package_successfully(self):
        params = valid_params()
        app_data = ApplicationData()

        command = CreatePackageCommand(params, app_data)
        command.execute()

        self.assertEqual(len(app_data.packages), 1)
        self.assertEqual(app_data.packages[0].weight, VALID_WEIGHT)
        self.assertEqual(app_data.packages[0].status, Status._class_status_types[0])
