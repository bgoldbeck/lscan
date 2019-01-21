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
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from pathlib import Path

class MetadataPanel(wx.Panel, IUIBehavior):
    """This class contains the wx widgets for control over metadata information in the
    program. These widgets may include, but not limited to author, license, stl file input,
    and ldraw file output.
    """
    text_ctrl_size = (400, 20)
    max_path_length = 256
    big_button = (120, 25)
    small_button_size = (30, 25)
    panel_size = (1024, 100)
    label_size = (150, 25)

    def __init__(self, parent):
        """Default constructor for MainPanel class.
        """
        wx.Panel.__init__(self, parent, size=self.panel_size, style=wx.BORDER_SUNKEN)
        self.parent = parent
        self.browse_stl_button = None
        self.help_button = None
        self.about_button = None
        self.browse_stl_button = None
        self.author_text = None
        self.license_text = None
        self._build_gui()
        self.parent.Layout()

        # Settings
        self.stl_dir = None
        self.part_name = None
        self.part_dir = None
        self.author = None
        self.license = None

    def _build_gui(self):
        """Initializing input, output, process control, and log panel elements
        :return:
        """
        self.SetBackgroundColour("#777fea")

        # Input
        path_name_static_text = wx.StaticText(
            self,
            label="Path to Input STL File",
            size=self.label_size,
            style=wx.ALIGN_RIGHT)

        # Stl input.
        self.stl_path_name_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.stl_path_name_text.SetMaxLength(self.max_path_length)

        self.browse_stl_button = wx.Button(self, label="Browse STL", size=self.big_button)

        # Help / About.
        self.help_button = wx.Button(self, label="?", size=self.small_button_size)
        self.about_button = wx.Button(self, label="i", size=self.small_button_size)

        # Output path selection.
        path_part_static_text = wx.StaticText(self, label="Part Name", size=self.label_size, style=wx.ALIGN_RIGHT)
        self.ldraw_name_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.ldraw_name_text.SetMaxLength(self.max_path_length)

        self.browse_output_button = wx.Button(self, label="Browse Output", size=self.big_button)

        # Author
        author_static_text = wx.StaticText(self, label="Author", size=self.label_size, style=wx.ALIGN_RIGHT)
        self.author_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.author_text.SetMaxLength(self.max_path_length)

        # License information.
        license_static_text = wx.StaticText(self, label="License", size=self.label_size, style=wx.ALIGN_RIGHT)
        self.license_text = wx.TextCtrl(self, size=self.text_ctrl_size)
        self.license_text.SetMaxLength(self.max_path_length)

        # Create the layout.
        horizontal_input = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_output = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_author = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_license = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_input.Add(path_name_static_text, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.stl_path_name_text, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.browse_stl_button, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.help_button, 0, wx.ALIGN_CENTER)
        horizontal_input.AddSpacer(5)
        horizontal_input.Add(self.about_button, 0, wx.ALIGN_CENTER)

        horizontal_output.Add(path_part_static_text, 0, wx.ALIGN_LEFT)
        horizontal_output.AddSpacer(5)
        horizontal_output.Add(self.ldraw_name_text, 0, wx.ALIGN_LEFT)
        horizontal_output.AddSpacer(5)
        horizontal_output.Add(self.browse_output_button, 0, wx.ALIGN_LEFT)

        horizontal_author.Add(author_static_text, 0, wx.ALIGN_LEFT)
        horizontal_author.AddSpacer(5)
        horizontal_author.Add(self.author_text, 0, wx.ALIGN_LEFT)

        horizontal_license.Add(license_static_text, 0, wx.ALIGN_LEFT)
        horizontal_license.AddSpacer(5)
        horizontal_license.Add(self.license_text, 0, wx.ALIGN_LEFT)

        vertical_layout = wx.BoxSizer(wx.VERTICAL)
        vertical_layout.Add(horizontal_input, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_output, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_author, 0, wx.ALIGN_LEFT)
        vertical_layout.Add(horizontal_license, 0, wx.ALIGN_LEFT)

        horizontal_split = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_split.AddSpacer(150)
        horizontal_split.Add(vertical_layout, 0, wx.ALIGN_LEFT)

        self.SetSizer(horizontal_split)

        # Register events.
        self.Bind(wx.EVT_BUTTON, self.about, self.about_button)
        self.Bind(wx.EVT_BUTTON, self.browse_output, self.browse_output_button)
        self.Bind(wx.EVT_BUTTON, self.help, self.help_button)
        self.Bind(wx.EVT_BUTTON, self.browse_input, self.browse_stl_button)

    def help(self, event):
        """Presents program limitations, common troubleshooting steps, and steps to update LDraw parts library.
        :param event:
        :return:
        """
        wx.MessageBox("""
            Program Limitations
            TEXT
            Troubleshooting
            TEXT
            How to update LDraw Parts Library
            TEXT""", "Help info", wx.OK | wx.ICON_QUESTION)

    def about(self, event):
        """Presents program name, program version, copyright information, licensing information, and authors to user.
        :param event:
        :return:
        """
        wx.MessageBox("""
            LScan
            Version 1.0
            Copyright (C) 2018 - This notice is to be included in all relevant source files.

            This software is licensed under the MIT License. See LICENSE file for the full text.

            Authors
            "Brandon Goldbeck" <bpg@pdx.edu>
            “Anthony Namba” <anamba@pdx.edu>
            “Brandon Le” <lebran@pdx.edu>
            “Ann Peake” <peakean@pdx.edu>
            “Sohan Tamang” <sohan@pdx.edu>
            “An Huynh” <an35@pdx.edu>
            “Theron Anderson” <atheron@pdx.edu>""", "About LScan", wx.OK | wx.ICON_INFORMATION)

    def browse_input(self, event):
        """Browse for a valid STL input file.
        :param event:
        :return:
        """
        stl_wildcard = "*.stl"
        #print(Path.cwd())
        dialog = wx.FileDialog(self, "Choose a STL file", defaultDir="", wildcard=stl_wildcard, style=wx.FD_OPEN
                               | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            # Check for file existing
            # If valid, pass to worker thread who will check data
            print(filename)
            #try:
            #    with open(filename, "r", encoding="utf-8") as file:
            #        stl_data = file.read()
            #        print(stl_data)
            #except IOError:
            #    print("IO ERROR!")
            #stl_data = self.get_file_text(dialog.GetCurrentlySelectedFilename)
            #print(stl_data)
        dialog.Destroy()

    def get_paste_input(self, event):
        """Get the path for STL input file from user typing into TextCtrl element.
        :param event:
        :return:
        """
        filepath = self.stl_path_name_text.GetValue()
        # Check file path validity
        print(filepath)

    def browse_output(self, event):
        """Browse for a valid DAT output file
        :param event:
        :return:
        """
        #temp_data = "this is temporary data remove this line when functional"
        ldraw_wildcard = "*.dat"
        dialog = wx.FileDialog(self, "Choose a location for the LDraw file", defaultDir="", wildcard=ldraw_wildcard,
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            pathname = dialog.GetPath()
            print(pathname)
            """
            try:
                with open(pathname, "w") as file:
                    file.write(temp_data)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)
            """
        dialog.Destroy()

    def get_file_output(self, event):
        """Get file output path from user in TextCtrl element.
        :param event:
        :return:
        """
        # Detect if you need to use:
        # default directory and default part name
        # current default directory and new part name
        # new part directory and new part name
        filepath = self.ldraw_name_text.GetValue()

        # File path is just a part name
        if not filepath.is_file():
            # Update settings file?

            # Append the default parts directory to the path
                # Read from settings file
            full_filepath = "DEFAULT PARTS DIRECTORY PATH" + filepath
            print(full_filepath)
        elif filepath.is_file():
            print(filepath)

    def get_author(self, event):
        """Get the author value from the user and update the settings file as needed."""
        author = self.author_text.GetValue()

        # Update settings file author info

        print(author)

    def get_license(self, event):
        """Get the license value from the user and update the settings file as needed."""
        license = self.license_text.GetVlaue()

        # Update settings file license info

        print(license)

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the MetadataPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        pass

    def on_event(self, event: UserEvent):
        """A user event was passed to the MetadataPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        pass

    def create_default_settings(self):
        """Generate initial settings file based on current working directory.
        """
        # default stl directory
        default_stl_dir = Path.cwd() / "assets/models/"
        # default part name
        default_part_name = "untitled.dat"
        # default part name directory
        default_part_dir = Path.cwd() / "assets/parts/"
        # default author
        default_author = "First Last "
        # default license
        default_license = "Redistributable under CCAL version 2.0 : see CAreadme.txt"

        settings = [default_stl_dir, default_part_name, default_part_dir, default_author, default_license]
        filepath = Path.cwd() / "assets/setting/user_settings.txt"

        if not filepath.is_file():
            with open(str(filepath), "a") as file:
                for setting in settings:
                    print(setting, file=file)

    def save_settings(self):
        """Save changes to user settings file.
        """
        # Determine changes to settings file
        # Write out changes to
        pass

    def read_settings(self):
        """Read the settings file."""
        filepath = Path.cwd() / "assets/setting/user_settings.txt"
        try:
            with open(str(filepath), "r") as file:
                settings = file.read()
                return settings
        except FileNotFoundError as ferr:
            print(ferr)

    def write_settings(self):
        """Write to the settings file."""
        pass

    def load_settings(self):
        """Load settings values into memory on startup."""
        pass
