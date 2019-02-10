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
from wx import glcanvas
from src.rendering.scene import Scene
from OpenGL.GL import *
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.iui_behavior import IUIBehavior
from src.model_conversion.model_shipper import ModelShipper
from pyrr import Vector3


class OpenGLCanvas(glcanvas.GLCanvas, IUIBehavior):
    """This is the canvas for OpenGL to render objects to.
    """
    canvas_size = (400, 300)

    def __init__(self, parent):
        """Default constructor for MainPanel class.
        """
        # Call the base constructor for the OpenGL canvas.
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.canvas_size)
        self.parent = parent
        self.context = None
        self.scene = None
        self.wire_frame = False
        self.interacted = False
        self.canvas_color = Vector3([0.0, 0.0, 0.3])
        self.init = False
        self.aspect_ratio = self.canvas_size[0] / self.canvas_size[1]

        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        """Event that occurs when the canvas paint event is called.
        :param event: the event that occurred.
        :return: None
        """
        wx.PaintDC(self)
        if not self.init:
            self.init_gl()
            self.init = True
        self.draw()

    def init_gl(self):
        """Initialize OpenGL functionality.
        :return: None
        """
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        glClearColor(self.canvas_color[0],  # Red
                     self.canvas_color[1],  # Green
                     self.canvas_color[2],  # Blue
                     1.0)  # Alpha

        glEnable(GL_DEPTH_TEST)

        glViewport(0, 0, self.canvas_size[0], self.canvas_size[1])
        self.scene = Scene(self)

    def draw(self):
        """Draw the previous OpenGL buffer with all the 3D data.
        :return: None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.wire_frame is True:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        self.Refresh()
        self.scene.update()
        self.scene.draw()
        self.SwapBuffers()

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the OpenGLCanvas.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        pass

    def on_event(self, event: UserEvent):
        """A user event was passed to the OpenGLCanvas.

        :param event: The recorded UserEvent.
        :return: None
        """
        if event is not None:
            if event.get_event_type() == UserEventType.INPUT_MODEL_READY:
                self.scene.replace_input_model_mesh(ModelShipper.input_model)
                self.scene.set_input_model_active(True)
            if event.get_event_type() == UserEventType.RENDERING_WIRE_FRAME_PRESSED:
                self.wire_frame = not self.wire_frame
