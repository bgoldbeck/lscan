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
import OpenGL.GL.shaders
from pyrr import Vector3
from src.rendering.rendering_engine import RenderingEngine


class Material:
    def __init__(self):
        self.shader = None

    def set_uniform_matrix4fv(self, key, value):
        # TODO: ensure key is a valid string. ensure value is a valid matrix 4x4
        assert self.shader is not None, "Shader program not set."
        glUniformMatrix4fv(glGetUniformLocation(self.shader, key), 1, GL_FALSE, value)

    def set_uniform1i(self, key, value):
        assert self.shader is not None, "Shader program not set."
        glUniform1i(glGetUniformLocation(self.shader, key), value)

    def set_uniform1f(self, key, value):
        assert self.shader is not None, "Shader program not set."
        glUniform1f(glGetUniformLocation(self.shader, key), value)

    def set_uniform2f(self, key, x, y):
        assert self.shader is not None, "Shader program not set."
        glUniform2f(glGetUniformLocation(self.shader, key), x, y)

    def set_uniform3f(self, key, value: Vector3):
        assert self.shader is not None, "Shader program not set."
        glUniform3f(glGetUniformLocation(self.shader, key),
                    value[0],
                    value[1],
                    value[2])
