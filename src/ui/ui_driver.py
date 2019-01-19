# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import wx
from src.ui.main_frame import MainFrame
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.iui_behavior import IUIBehavior


class UIDriver:
    """

    """

    instance = None
    application_state = None
    root_frame = None

    def __init__(self):
        if not UIDriver.instance:
            UIDriver.instance = self
            UIDriver.root_frame = MainFrame()
            UIDriver.root_frame.Show()
            UIDriver.change_application_state(ApplicationState.STARTUP)

    @staticmethod
    def get_instance():
        """

        :return:
        """
        if not UIDriver.instance:
            UIDriver.instance = UIDriver()
        return UIDriver.instance

    @staticmethod
    def get_all_ui_behaviors(root, behaviors):
        """

        :param root:
        :param behaviors:
        :return:
        """
        if root is None:
            return

        children = root.GetChildren()

        for child in children:
            if isinstance(child, IUIBehavior):
                behaviors.append(child)
            UIDriver.get_all_ui_behaviors(child, behaviors)

    @staticmethod
    def fire_event(event: UserEvent):
        """

        :param event:
        :return:
        """
        # We need to notify all the ui behaviors of the event.
        ui_behaviors = []
        UIDriver.get_all_ui_behaviors(UIDriver.root_frame, ui_behaviors)

        for ui_behavior in ui_behaviors:
            ui_behavior.on_event(event)

    @staticmethod
    def change_application_state(new_state: ApplicationState):
        """

        :param new_state:
        :return:
        """
        # Set the new state.
        UIDriver.application_state = new_state

        # Notify all the ui behavior objects of the state change.
        ui_behaviors = []
        UIDriver.get_all_ui_behaviors(UIDriver.root_frame, ui_behaviors)

        for ui_behavior in ui_behaviors:
            ui_behavior.on_state_changed(new_state)
