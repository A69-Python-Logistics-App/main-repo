import unittest
from models.Status import Status

INIT_VALID_STATUS = "Collected"
INIT_VALID_IDX = 0

VALID_STATUS_ON_ROUTE = "On Route"
VALID_STATUS_DELIVERED = "Delivered"

class Status_Should(unittest.TestCase):

    def test_status_initializer_shouldSet_validParams(self):
        # ARRANGE + ACT
        status = Status()
        # ASSERT
        self.assertEqual(INIT_VALID_STATUS, status.current)
        self.assertEqual(INIT_VALID_IDX, status._idx)

    def test_advanceStatus_should_advanceStatusCorrectly(self):
        # ARRANGE
        status = Status()
        # ACT + ASSERT
        status.advance_status()
        self.assertEqual(VALID_STATUS_ON_ROUTE, status.current)
        # ACT + ASSERT
        status.advance_status()
        self.assertEqual(VALID_STATUS_DELIVERED, status.current)

    def test_advanceStatus_staysTheSame_when_statusAlreadyDelivered(self):
        # ARRANGE
        status = Status()
        # ACT + ASSERT
        status.advance_status()
        status.advance_status()
        status.advance_status()
        status.advance_status()
        self.assertEqual(VALID_STATUS_DELIVERED, status.current)
        status.advance_status()
        self.assertEqual(VALID_STATUS_DELIVERED, status.current)
