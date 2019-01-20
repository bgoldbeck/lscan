import unittest
import wx
from src.ui.ui_driver import UIDriver
from src.lscan import LScan
from src.ui.application_state import ApplicationState
from src.ui.main_frame import MainFrame


class UIDriverTest(unittest.TestCase):
    def setUp(self):
        self.ui_driver = UIDriver(None)

    def tearDown(self):
        pass

    def testInitialized(self):
        self.assertIsNone(self.ui_driver.root_frame)
        self.assertEqual(self.ui_driver.application_state, ApplicationState.WAITING_INPUT)
        self.assertEqual(self.ui_driver.instance, self.ui_driver)


