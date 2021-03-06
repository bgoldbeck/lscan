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
import sys
from src.ui.main_panel import MainPanel
from src.ui.ui_style import UIStyle


class MainFrame(wx.Frame):
    """The root Wx Frame that will be the parent of all Wx controls.
    """

    def __init__(self):
        """Default constructor for MainFrame class.
        """
        wx.Frame.__init__(self, None, title="LScan", size=UIStyle.main_frame_size,
                          style=UIStyle.main_frame_border |
                                wx.FULL_REPAINT_ON_RESIZE | wx.MINIMIZE_BOX)

        UIStyle.setup_dark_theme()  # Overwrite the default color
        self._build_gui()

    def _build_gui(self):
        """Create all the sub-panels and their layout on this main panel.
        :return: None
        """
        # Set the limitations on the frame.
        self.SetMinSize(UIStyle.main_frame_size)
        self.SetMaxSize(UIStyle.main_frame_size)

        # Application needs to be able to close.
        self.Bind(wx.EVT_CLOSE, self._on_close)

        # Create a MainPanel instance, pass ourselves to the constructor to make
        # this MainFrame the parent.
        self.panel = MainPanel(self)

    def _on_close(self, event):
        """Called when the user clicks the close button on the frame.

        :param event: the event that was recorded by WxPython
        :return: None
        """
        print(event)
        self.Destroy()
        sys.exit(0)
