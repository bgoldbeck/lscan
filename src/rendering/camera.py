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
from pyrr import Vector3, Matrix44, vector, vector3
from src.rendering.scene_object import SceneObject


# Code is attributed to totex/PyOpenGL_season_02
# -Attila Toth from GitHub.
class Camera(SceneObject):
    def __init__(self, tag):
        """

        """
        SceneObject.__init__(self, tag)
        self.transform.position = Vector3([0.0, 0.0, 20.0])
        self.target = Vector3([0.0, 0.0, 0.0])
        self.mouse_sensitivity = 0.25
        self.transform.eulerAngles = Vector3([0.0, 0.0, 0.0])

    def get_view_matrix(self):
        return self.transform.look_at(self.target)

    def draw(self):
        pass

    def update(self):
        pass

