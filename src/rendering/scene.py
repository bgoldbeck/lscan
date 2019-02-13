# Copyright (C) 2018
# This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License.
# See LICENSE file for the full text.
from src.rendering.basic_mesh_object import BasicMeshObject
from src.rendering.camera import Camera
from src.rendering.rendering_engine import RenderingEngine
from src.rendering.tranform import Transform
from pyrr import Vector3, Vector4, Matrix44

import time, wx, math


class Scene:
    _last_time = 0.0
    _ang_x = 0
    _ang_y = 0
    _camera_distance = 10.0
    _current_model_context = None

    def __init__(self, gl_canvas):
        self.last_mouse_position = (0.0, 0.0)
        self.delta_mouse = (0.0, 0.0)
        self._last_time = time.process_time()
        self.active_scene_object = None

        self.scene_objects = {
            "camera": Camera("camera"),
            "input_model": None,
            "output_model": None
        }

        RenderingEngine.camera = self.scene_objects["camera"]

    def on_mouse_move(self, event):
        """

        :param event:
        :return:
        """
        point = event.GetPosition()
        if self.last_mouse_position == (0.0, 0.0):
            self.last_mouse_position = point

        if event.Dragging():
            self.delta_mouse = (
                point[0] - self.last_mouse_position[0],  # dx
                point[1] - self.last_mouse_position[1])  # dy

        self.last_mouse_position = point

    def on_mouse_wheel(self, event):
        """

        :param event:
        :return:
        """
        self._camera_distance -= event.GetWheelRotation() / 500.0
        event.Skip()

    def draw(self):
        for key, scene_object in self.scene_objects.items():
            if scene_object is not None:
                scene_object.draw()

    def update(self):
        RenderingEngine.delta_time = time.process_time() - self._last_time
        self._last_time = time.process_time()

        self._ang_x -= self.delta_mouse[0] * 0.7
        self._ang_y += self.delta_mouse[1] * 0.7

        self._ang_y = Transform.clamp_angle(self._ang_y, -85.0, 85.0)

        rotation = Transform.euler_to_quaternion(
            self._ang_y,
            self._ang_x,
            0.0)

        q0 = Transform.mult_quaternion_by_vector(
            rotation,
            (Vector3([0.0, 0.0, -1.0]) * self._camera_distance))

        if self.active_scene_object is not None:
            RenderingEngine.camera.transform.position = \
                self.active_scene_object.transform.position + q0

        for key, scene_object in self.scene_objects.items():
            if scene_object is not None:
                if scene_object.enabled:
                    scene_object.update()

        self.delta_mouse = (0.0, 0.0)

    def get_scene_object(self, tag):
        return self.objects[tag]

    def replace_input_model_mesh(self, mesh):
        self._replace_model_mesh("input_model", mesh)

    def replace_output_model_mesh(self, mesh):
        self._replace_model_mesh("output_model", mesh)

    def _replace_model_mesh(self, tag, mesh):
        self.remove_scene_object(tag)
        self.scene_objects.update({tag: BasicMeshObject(tag, mesh)})
        self.scene_objects[tag].transform.position = Vector3([0.0, 0.0, 0.0])

    def set_input_model_active(self, value):
        self._set_model_active("input_model", value)

    def set_output_model_active(self, value):
        self._set_model_active("output_model", value)

    def _set_model_active(self, tag, value):
        if self.scene_objects[tag] is not None:
            if value is True:
                self.active_scene_object = self.scene_objects[tag]
                self.scene_objects[tag].enable()
            else:
                self.scene_objects[tag].disable()
        self._current_model_context = self.scene_objects[tag]

    def remove_scene_object(self, tag):
        if self.scene_objects.get(tag) is not None:
            self.scene_objects.pop(tag)

    def get_main_camera(self):
        return RenderingEngine.camera

    def get_camera_distance_to_origin(self):
        return self._camera_distance

    def get_current_model_scale(self):
        return self._current_model_context.transform.scale

    def set_model_scale(self, scale: float):
        input_model = self.scene_objects["input_model"]
        output_model = self.scene_objects["output_model"]
        scale_vector = Vector3([scale, scale, scale])

        if input_model is not None:
            input_model.transform.scale = scale_vector
        if output_model is not None:
            output_model.transform.scale = scale_vector

