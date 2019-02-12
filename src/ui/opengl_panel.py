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
from src.log_messages.float_message import FloatMessage
from src.log_messages.bool_message import BoolMessage
from src.log_messages.log_type import LogType
from src.ui.ui_style import *
from src.rendering.scene import Scene


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

        #self.wf_btn = wx.Button(self, label="Wireframe", size=UI_style.conversion_big_button_size)
        #self.wf_btn.SetBackgroundColour(UI_style.button_background)
        #self.wf_btn.SetForegroundColour(UI_style.button_text)

        self.cb_wireframe = wx.CheckBox(self, label=" Wireframe")
        self.cb_wireframe.SetForegroundColour(UI_style.metadata_label_color)

        self.zoom_static_text_ctrl = wx.StaticText(self, size=UI_style.metadata_label_size)
        self.zoom_static_text_ctrl.SetLabelText("Camera Distance to Origin: ")
        self.zoom_static_text_ctrl.SetForegroundColour(UI_style.metadata_label_color)

        self.scale_static_text = wx.StaticText(self, label="Scale:", size=(50, 20))
        self.scale_static_text.SetForegroundColour(UI_style.metadata_label_color)

        self.scale_up_button = wx.Button(self, label="+", size=(20, 20))
        self.scale_down_button = wx.Button(self, label="-", size=(20, 20))
        self.scale_input = wx.TextCtrl(self, size=(100, 20))
        #self.scale_input.SetMaxLength(self.max_path_length)
        self.scale_input.SetBackgroundColour(UI_style.metadata_input_valid_background)
        self.scale_input.SetForegroundColour(UI_style.metadata_input_text_color)

        self.opengl_canvas = OpenGLCanvas(self)

        # Layout the UI
        # Left Side

        left_vertical_layout = wx.BoxSizer(wx.VERTICAL)
        left_vertical_layout.Add(self.cb_wireframe, 0, wx.ALIGN_LEFT)
        left_vertical_layout.AddSpacer(10)
        left_vertical_layout.Add(self.scale_static_text, 0, wx.ALIGN_LEFT)
        scale_horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        scale_horizontal_layout.Add(self.scale_down_button, 0, wx.ALIGN_LEFT)
        scale_horizontal_layout.Add(self.scale_input, 0, wx.ALIGN_LEFT)
        scale_horizontal_layout.Add(self.scale_up_button, 0, wx.ALIGN_LEFT)
        scale_horizontal_layout.AddSpacer(150)
        left_vertical_layout.Add(scale_horizontal_layout)

        horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_layout.Add(left_vertical_layout)
        #horizontal_layout.AddSpacer(50)


        # Middle
        horizontal_layout.Add(self.opengl_canvas, 0, wx.ALIGN_CENTER_HORIZONTAL)
       #horizontal_layout.AddSpacer(5)

        # Right Side
        right_vertical_layout = wx.BoxSizer(wx.VERTICAL)
        horizontal_layout.Add(self.zoom_static_text_ctrl, 0, wx.ALIGN_CENTER_HORIZONTAL)
        #horizontal_layout.AddSpacer(5)

        self.SetSizer(horizontal_layout)

        # Bind events to functions.
        self.Bind(wx.EVT_CHECKBOX, self.on_wire_frame_pressed, self.cb_wireframe)

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
        if event is not None:
            if event.get_event_type() == UserEventType.RENDERING_MOUSE_WHEEL_EVENT:
                # Log Message here is of derived class FloatMessage.
                if isinstance(event.get_log_message(), FloatMessage):
                    self.zoom_static_text_ctrl.SetLabelText(
                        "Camera Distance to Origin: " + str(event.get_log_message().get_float()))
            elif event.get_event_type() == UserEventType.INPUT_MODEL_READY:
                    self.zoom_static_text_ctrl.SetLabelText(
                        "Camera Distance to Origin: " + str(self.opengl_canvas.scene.get_camera_distance_to_origin()))

    def on_wire_frame_pressed(self, event):
        """Send an event that the wireframe button was pressed. The OpenGLCanvas will
        detect and react accordingly.

        :param event: The wxpython event that occured.
        :return:
        """
        UIDriver.fire_event(UserEvent(
            UserEventType.RENDERING_WIRE_FRAME_PRESSED,
            BoolMessage(
                LogType.DEBUG, "Wire frame checkbox pressed.",
                self.cb_wireframe.GetValue())
        ))
        event.Skip()
