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
from OpenGL.GL import *
from stl import mesh
from pyrr import *
from src.rendering.basic_material import BasicMaterial
from src.rendering.scene_object import SceneObject
from src.rendering.rendering_engine import RenderingEngine
import random
import numpy
import time

class BasicMeshObject(SceneObject):
    def __init__(self, tag, file_path):
        """
        """
        SceneObject.__init__(self, tag)

        # TODO: confirm valid filepath
        self.mesh_data = mesh.Mesh.from_file(file_path)
        triangle_data = []

        for i in range(len(self.mesh_data.normals)):
                triangle_data.append(self.mesh_data.v2[i][0])
                triangle_data.append(self.mesh_data.v2[i][1])
                triangle_data.append(self.mesh_data.v2[i][2])
                triangle_data.append(0.000059)
                triangle_data.append(1.0 - 0.000059)
                triangle_data.append(self.mesh_data.normals[i][0])
                triangle_data.append(self.mesh_data.normals[i][1])
                triangle_data.append(self.mesh_data.normals[i][2])
                triangle_data.append(self.mesh_data.v1[i][0])
                triangle_data.append(self.mesh_data.v1[i][1])
                triangle_data.append(self.mesh_data.v1[i][2])
                triangle_data.append(0.000103)
                triangle_data.append(1.0 - 0.336048)
                triangle_data.append(self.mesh_data.normals[i][0])
                triangle_data.append(self.mesh_data.normals[i][1])
                triangle_data.append(self.mesh_data.normals[i][2])
                triangle_data.append(self.mesh_data.v0[i][0])
                triangle_data.append(self.mesh_data.v0[i][1])
                triangle_data.append(self.mesh_data.v0[i][2])
                triangle_data.append(0.335973)
                triangle_data.append(1.0 - 0.335903)
                triangle_data.append(self.mesh_data.normals[i][0])
                triangle_data.append(self.mesh_data.normals[i][1])
                triangle_data.append(self.mesh_data.normals[i][2])

        self.vao = glGenVertexArrays(1)

        self.bind()
        self.material = BasicMaterial(numpy.array(triangle_data, dtype=numpy.float32))
        self.unbind()

    def bind(self):
        glBindVertexArray(self.vao)

    def unbind(self):
        glBindVertexArray(0)

    def draw(self):
        self.bind()
        glDrawArrays(GL_TRIANGLES, 0, len(self.mesh_data.normals) * 3)
        self.unbind()

    def update(self):
        self.material.set_view_matrix(RenderingEngine.camera.get_view_matrix())
        self.material.set_model_matrix(self.transform.get_trs_matrix())

    def get_mesh_data(self):
        return self.mesh_data
