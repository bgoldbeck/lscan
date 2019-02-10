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
    _camera_distance = 20.0

    def __init__(self, gl_canvas):
        self.last_mouse_position = (0.0, 0.0)
        self.delta_mouse = (0.0, 0.0)
        self._last_time = time.process_time()
        self.active_scene_object = None
        self.scene_objects = {
            "camera": Camera("camera"),
        #    "plane_model": BasicMeshObject("stl_model", "assets/models/plane.stl"),
        #    "cube_model": BasicMeshObject("stl_model", "assets/models/cube.stl")
        }

        RenderingEngine.camera = self.scene_objects["camera"]
        #RenderingEngine.camera.position = Vector3([0.0, 0.0, -22.0])
        #RenderingEngine.camera.transform.look_at(Vector3([0.0, 0.0, 0.0]))

        #self.scene_objects["cube_model"].transform.position = Vector3([0.0, 0.0, 0.0])

        #self.scene_objects["stl_model"].transform.rotate_position_around_point(
        #    Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0]), 45.0)

        #self.scene_objects["stl_model"].transform.look_at(
        #    Vector3([0.0, 0.0, 0.0]))

        gl_canvas.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        gl_canvas.Bind(wx.EVT_MOTION, self.on_mouse_move)

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
        self._camera_distance -= event.GetWheelRotation() / 70.0

    def draw(self):
        for key, scene_object in self.scene_objects.items():
            scene_object.draw()

    def update(self):
        RenderingEngine.delta_time = time.process_time() - self._last_time
        self._last_time = time.process_time()

        #self.scene_objects["stl_model"].transform.rotate_position_around_point(
        #    Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0]), 0.5)

        self._ang_x -= self.delta_mouse[0] * 0.7
        self._ang_y += self.delta_mouse[1] * 0.7

        self._ang_y = Transform.clamp_angle(self._ang_y, -85.0, 85.0)
        #self._ang_x = Transform.clamp_angle(self._ang_x)
        #self._ang_x = 210.0
        #self._ang_y = 310.0

        print(self._ang_y)

        #self._ang_x = 45.0
        #self._ang_y = 45.0

        rotation = Transform.euler_to_quaternion(
            self._ang_y,
            self._ang_x,
            0.0)


        #position = Transform.mult_quaternion_by_vector(rotation, Vector3([0.0, 0.0, -self._camera_distance])) + self.scene_objects["cube_model"].transform.position

        #position = Vector3((0.0, 0.0, -5.0))
        #RenderingEngine.camera.transform.position = position
        #RenderingEngine.camera.transform.rotation_from_quaternion(rotation)

        #print(position)
        #print(rotation)

        #RenderingEngine.camera.transform.look_at(self.scene_objects["stl_model"].transform.position)
        #RenderingEngine.camera.transform.position = rotation * Vector4([0.0, 0.0, -20.0, 1.0]) + Vector4.from_vector3(self.scene_objects["stl_model"].transform.position)

        #RenderingEngine.camera.transform.euler_angles = Vector3(Transform.quaternion_to_euler(rotation))

        q0 = Transform.mult_quaternion_by_vector(
            rotation,
            (Vector3([0.0, 0.0, -1.0]) * self._camera_distance))

        #print(q0)

        if self.active_scene_object is not None:
            RenderingEngine.camera.transform.position = \
                self.active_scene_object.transform.position + q0

        for key, scene_object in self.scene_objects.items():
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

    def remove_scene_object(self, tag):
        if self.scene_objects.get(tag) is not None:
            self.scene_objects.pop(tag)

