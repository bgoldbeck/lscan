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
from pyrr import *

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
        self.scene_objects = {
            "camera": Camera("camera"),
            "plane_model": BasicMeshObject("stl_model", "assets/models/plane.stl"),
            "cube_model": BasicMeshObject("stl_model", "assets/models/cube.stl")}

        RenderingEngine.camera = self.scene_objects["camera"]
        #RenderingEngine.camera.position = Vector3([0.0, 0.0, -22.0])
        #RenderingEngine.camera.transform.look_at(Vector3([0.0, 0.0, 0.0]))

        self.scene_objects["cube_model"].transform.position = Vector3([0.0, 0.0, 0.0])

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
        print(event.GetWheelRotation())

        self._camera_distance -= event.GetWheelRotation() / 70.0

    def draw(self):
        for key, scene_object in self.scene_objects.items():
            scene_object.draw()

    def update(self):
        RenderingEngine.delta_time = time.process_time() - self._last_time
        self._last_time = time.process_time()

        #self.scene_objects["stl_model"].transform.rotate_position_around_point(
        #    Vector3([0.0, 0.0, 0.0]), Vector3([0.0, 1.0, 0.0]), 0.5)

        self._ang_x -= self.delta_mouse[0] * 0.2
        self._ang_y += self.delta_mouse[1] * 0.2

        self._ang_y = Transform.clamp_angle(self._ang_y, 10.0, 80.0)
        self._ang_x = Transform.clamp_angle(self._ang_x)
        #self._ang_x = 45.0
        #self._ang_y = 45.0

        rotation = Quaternion(Transform.euler_to_quaternion(
            self._ang_y,
            self._ang_x,
            0.0))

        position = Transform.mult_quaternion_by_vector(rotation, Vector3([0.0, 0.0, -self._camera_distance])) + self.scene_objects["cube_model"].transform.position

        RenderingEngine.camera.transform.position = position
        RenderingEngine.camera.transform.rotation_from_quaternion(rotation)

        #print(position)
        #print(rotation)

        #RenderingEngine.camera.transform.look_at(self.scene_objects["stl_model"].transform.position)
        #RenderingEngine.camera.transform.position = rotation * Vector4([0.0, 0.0, -20.0, 1.0]) + Vector4.from_vector3(self.scene_objects["stl_model"].transform.position)

        #RenderingEngine.camera.transform.euler_angles = Vector3(Transform.quaternion_to_euler(rotation))


        #RenderingEngine.camera.transform.position = self.scene_objects["stl_model"].transform.position + (Transform.mult_quaternion_by_vector(rotation, (Vector3([0.0, 0.0, -1.0]) * self._camera_distance)))


        #print(self._ang_y)
        #print(self._ang_x)
        #print(RenderingEngine.camera.transform.euler_angles)
        #print(quaternion.rotation_axis(rotation))

#

#        RenderingEngine.camera.transform.rotation(rotation[0], rotation[1], rotation[2])

        #print(rotation)
        #print(RenderingEngine.camera.transform.position)


        #RenderingEngine.camera.transform.rotate_position_around_point(
        #    Vector3([0.0, 0.0, 0.0]),
        #    Vector3([1.0, 0.0, 0.0]),
        #    self.delta_mouse[1])

        #self.scene_objects["stl_model"].transform.rotate(
        #    0.0,
        #    self.delta_mouse[0],
        #    0.0)

#        RenderingEngine.camera.transform.rotate_position_around_point(
#            Vector3([0.0, 0.0, 0.0]),
#            Vector3([0.0, 0.0, -1.0]),
#            self.delta_mouse[1] * RenderingEngine.delta_time * 75.0)


        for key, scene_object in self.scene_objects.items():
            scene_object.update()

        self.delta_mouse = (0.0, 0.0)

    def get_scene_object(self, tag):
        return self.objects[tag]
