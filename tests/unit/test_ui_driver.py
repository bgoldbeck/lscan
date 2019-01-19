import unittest
import wx
from src.ui.ui_driver import UIDriver
from src.lscan import LScan
from src.ui.application_state import ApplicationState


class UIDriverTest(unittest.TestCase):
    def setUp(self):
        app = LScan()
        self.ui_driver = UIDriver()

    def tearDown(self):
        pass

    def testInitialized(self):
        self.assertIsNotNone(self.ui_driver.root_frame)
        self.assertIsNotNone(self.ui_driver.root_frame)
        self.assertEqual(self.ui_driver.application_state, ApplicationState.WAITING_INPUT)


