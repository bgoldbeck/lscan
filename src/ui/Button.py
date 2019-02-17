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


class Button(wx.Button):
    """This panel controls the behavior for the output log panel that will display
    running information to the user about the programs progress while running
    various algorithms.
    """
    _log_file_path = "log.txt"

    def __init__(self, parent, id=wx.ID_ANY, label="", size=(100, 20), pos=wx.DefaultPosition):
        """Default constructor for MainPanel class.

        :param parent: The parent wx object for this panel.
        """
        wx.Button.__init__(self, parent, size=size, id=id, label=label, pos=pos)

    def Enable(self):
        super().Enable()
        self.SetLabelText(self.GetLabelText())

    def Disable(self):
        super().Disable()
        self.SetLabelText(self.GetLabelText())
