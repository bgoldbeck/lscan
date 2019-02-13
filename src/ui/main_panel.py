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
from src.ui.log_panel import LogPanel
from src.ui.conversion_panel import ConversionPanel
from src.ui.opengl_panel import OpenGLPanel
from src.ui.metadata_panel import MetadataPanel
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.ui_style import *


class MainPanel(wx.Panel, IUIBehavior):
    """The child of the MainFrame. This panel will hold the main applications sub-panels.
    """

    def __init__(self, parent):
        """Default constructor for MainPanel class.

        :param parent: The parent wx object that will be the parent of this main panel.
        """
        wx.Panel.__init__(self, parent, size=parent.GetSize())
        self.parent = parent
        self.opengl_panel = None
        self.log_panel = None
        self.metadata_panel = None
        self.conversion_panel = None
        self.setup_dark_theme()  # Overwrite the default color
        self._build_gui()

    def _build_gui(self):
        """Create all the sub-panels and their layout on this main panel.
        :return: None
        """
        self.SetBackgroundColour(UIStyle.main_panel_background_color)

        # Create the sub-panels
        self.metadata_panel = MetadataPanel(self)
        self.conversion_panel = ConversionPanel(self)
        self.log_panel = LogPanel(self)
        self.opengl_panel = OpenGLPanel(self)

        # Create the layout of the sub-panels.
        vertical_layout = wx.BoxSizer(wx.VERTICAL)
        vertical_layout.Add(self.metadata_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(self.opengl_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(self.conversion_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
        vertical_layout.Add(self.log_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(vertical_layout)

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the MainPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        pass

    def on_event(self, event: UserEvent):
        """A user event was passed to the MainPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass

    def setup_dark_theme(self):
        """Set up dark color theme for program.
        """
        # Utility
        # UIStyle.button_background = "#2B2B2B"
        # UIStyle.button_text = "#A9B7C6"

        # Main Frame
        UIStyle.main_frame_border = wx.DEFAULT_FRAME_STYLE
        UIStyle.main_frame_min_size = (1024, 640)
        UIStyle.main_frame_max_size = (1024, 900)
        UIStyle.main_frame_current_size = UIStyle.main_frame_min_size

        # Main Panel
        UIStyle.main_panel_background_color = "#2B2B2B"

        # Metadata Panel
        UIStyle.metadata_border = wx.BORDER_NONE
        UIStyle.metadata_background_color = "#2B2B2B"
        UIStyle.metadata_label_color = "#808080"
        UIStyle.metadata_input_text_color = "#A5C25C"
        UIStyle.metadata_input_valid_background = "#323232"
        UIStyle.metadata_input_invalid_background = "#D25252"

        UIStyle.metadata_text_ctrl_size = (400, 20)
        UIStyle.metadata_big_button = (120, 25)
        UIStyle.metadata_small_button_size = (30, 25)
        UIStyle.metadata_panel_size = (1024, 100)
        UIStyle.metadata_label_size = (200, 25)

        # Conversion Panel
        UIStyle.conversion_border = wx.BORDER_NONE
        UIStyle.conversion_background_color = "#2B2B2B"
        UIStyle.conversion_big_button_size = (120, 30)

        # Log Panel
        UIStyle.log_border = wx.BORDER_NONE
        UIStyle.log_background_color = "#2B2B2B"
        UIStyle.log_text_background_color = "#323232"
        UIStyle.log_default_text_color = "#A9B7C6"
        UIStyle.log_info_text_color = "white"
        UIStyle.log_warning_text_color = "#FFC66D"
        UIStyle.log_debug_text_color = "#BED6FF"
        UIStyle.log_error_text_color = "#D25252"

        UIStyle.log_big_button = (70, 25)
        UIStyle.log_output_size = (920, 165)
        UIStyle.log_panel_size = (1022, 500)
        UIStyle.log_font_size = 10

        # OpenGL Panel


    def update(self, dt: float):
        pass
