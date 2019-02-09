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
from src.ui.opengl_canvas import OpenGLCanvas
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.ui_driver import UIDriver
from src.log_messages.log_message import LogMessage
from src.log_messages.log_type import LogType
from src.ui.ui_style import *


class OpenGLPanel(wx.Panel, IUIBehavior):
    """Holds wx controls relevant to controlling the program behavior for starting, stopping,
    pausing, and canceling the conversion process.
    """

    def __init__(self, parent):
        """Default constructor for ConversionPanel class.

        :param parent: The parent wx object for this panel.
        """
        wx.Panel.__init__(self, parent, size=(1024, 300), style=UI_style.conversion_border)
        self.parent = parent
        self.wf_btn = None
        self._build_gui()

    def _build_gui(self):
        """Initializing wx objects that make up this conversion panel and their layout within.

        :return: None
        """
        print("test")
        #self.SetBackgroundColour("#111eee")
        self.wf_btn = wx.Button(self, label="Wireframe", size=UI_style.conversion_big_button_size)
        self.wf_btn.SetBackgroundColour(UI_style.button_background)
        self.wf_btn.SetForegroundColour(UI_style.button_text)
        self.opengl_canvas = OpenGLCanvas(self)


        horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_layout.Add(self.wf_btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.Add(self.opengl_canvas, 0, wx.ALIGN_CENTER_HORIZONTAL)
        horizontal_layout.AddSpacer(5)

        self.SetSizer(horizontal_layout)

        # Bind events to functions.
        self.Bind(wx.EVT_BUTTON, self.on_wire_frame_pressed, self.wf_btn)

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the ConversionPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        pass

    def on_event(self, event: UserEvent):
        """A user event was passed to the ConversionPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass

    def on_wire_frame_pressed(self, event):
        """Send an event that the wireframe button was pressed. The OpenGLCanvas will
        detect and react accordingly.

        :param event: The wxpython event that occured.
        :return:
        """
        UIDriver.fire_event(UserEvent(
            UserEventType.RENDERING_WIRE_FRAME_PRESSED,
            LogMessage(
                LogType.DEBUG, "Wire frame button pressed.")
        ))
        event.Skip()
