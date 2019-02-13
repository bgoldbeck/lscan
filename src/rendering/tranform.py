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
from pyrr import Vector3, Vector4, Matrix44, vector3
import math
import numpy as np
from pyquaternion import Quaternion


class Transform:
    """The class that controls information about a transform.
    """
    euler_angles = Vector3([0.0, 0.0, 0.0])
    position = Vector3([0.0, 0.0, 0.0])
    scale = Vector3([1.0, 1.0, 1.0])

    forward = Vector3([0.0, 0.0, 1.0])
    up = Vector3([0.0, 1.0, 0.0])
    right = Vector3([1.0, 0.0, 0.0])

    def __init__(self):
        pass

    def translate(self, direction, distance):
        """Translate this transform a direction by a distance.

        :param direction: The direction to translate.
        :param distance: The distance to translate.
        :return:
        """
        self.position += direction * distance

    def look_at(self, target: Vector3):
        """Make this transform look at a particular point.

        :param target: The target point to look at.
        :return: Matrix44: The new rotation matrix.
        """
        heading = Vector3(target - self.position)
        heading.normalise()

        pitch = math.asin(heading[1]) * (180.0 / math.pi)
        yaw = math.atan2(heading[0], heading[2]) * (180.0 / math.pi)

        # Roll will always be zero when using this function.
        roll = 0.0

        self.euler_angles = Vector3([pitch, yaw, roll])

        rot_mat = Matrix44.look_at(self.position,
                                   target,
                                   self.world_up())

        self.forward = rot_mat * Vector4.from_vector3(self.world_forward(), w=0.0)
        self.forward = Vector3.from_vector4(Vector4(self.forward))[0]

        self.up = rot_mat * Vector4.from_vector3(self.world_up(), w=0.0)
        self.up = Vector3.from_vector4(Vector4(self.up))[0]

        self.right = rot_mat * Vector4.from_vector3(-self.world_right(), w=0.0)
        self.right = Vector3.from_vector4(Vector4(self.right))[0]

        return rot_mat

    def _get_rotation_matrix(self):
        """Retrieve the rotation matrix

        :return: Matrix44: The rotation matrix stored in this transform.
        """
        self.euler_angles[0] = self.clamp_angle(self.euler_angles[0])
        self.euler_angles[1] = self.clamp_angle(self.euler_angles[1])
        self.euler_angles[2] = self.clamp_angle(self.euler_angles[2])

        return Matrix44.from_eulers(self.euler_angles)

    def get_trs_matrix(self):
        """Retrieve the translation-rotation-scaling matrix

        :return: Matrix44: The translation-rotation-scaling matrix stored in this transform.
        """
        # Scale
        scale_matrix = Matrix44.from_scale(self.scale)

        # Rotate
        rs_matrix = scale_matrix * self._get_rotation_matrix()

        # Translate
        trs_matrix = rs_matrix * Matrix44.from_translation(self.position)

        return trs_matrix

    @staticmethod
    def clamp_angle(angle, min_angle=0.0, max_angle=360.0):
        """Clamp an angle value between a minimum and maximum range.

        :param angle: The angle to clamp.
        :param min_angle: The minimum angle.
        :param max_angle: The maximum angle.
        :return:
        """
        if angle > 360:
            angle = 360 - angle

        angle = max(min(angle, max_angle), min_angle)

        if angle < -360:
            angle = 360 + angle

        return angle

    @staticmethod
    def world_forward():
        """Retrieve the default world forward vector.

        :return: Vector3: The world forward as a Vector3.
        """
        return Vector3([0.0, 0.0, 1.0])

    @staticmethod
    def world_up():
        """Retrieve the default world up vector.

        :return: Vector3: The world up as a Vector3.
        """
        return Vector3([0.0, 1.0, 0.0])

    @staticmethod
    def world_right():
        """Retrieve the default world right vector.

        :return: Vector3: The world right as a Vector3.
        """
        return Vector3([1.0, 0.0, 0.0])

    @staticmethod
    def euler_to_quaternion(roll, pitch, yaw):
        """Convert a roll, pitch, and yaw value to a quaternion Vector.

        :param roll: The roll of the euler angles.
        :param pitch: The pitch of the euler angles.
        :param yaw: The yaw of the euler angles.
        :return: An array of length 4 containing the quaternion values. [x, y, z, w]
        """
        pitch = pitch * (math.pi / 180.0)
        yaw = yaw * (math.pi / 180.0)
        roll = roll * (math.pi / 180.0)
        r2 = roll / 2
        p2 = pitch / 2
        y2 = yaw / 2
        qx = np.sin(r2) * np.cos(p2) * np.cos(y2) - np.cos(r2) * np.sin(p2) * np.sin(y2)
        qy = np.cos(r2) * np.sin(p2) * np.cos(y2) + np.sin(r2) * np.cos(p2) * np.sin(y2)
        qz = np.cos(r2) * np.cos(p2) * np.sin(y2) - np.sin(r2) * np.sin(p2) * np.cos(y2)
        qw = np.cos(r2) * np.cos(p2) * np.cos(y2) + np.sin(r2) * np.sin(p2) * np.sin(y2)

        return [qx, qy, qz, qw]

    @staticmethod
    def mult_quaternion_by_vector(q1, v1: Vector3):
        """Multiply a quaternion by a standard vector.

        :param q1: The quaternion
        :param v1: The vector.
        :return: The resulting vector from the multiplication.
        """
        q1 = Quaternion(q1[3], q1[0], q1[1], q1[2])
        result = q1.rotate(v1)

        return result

    @staticmethod
    def quaternion_conjugate(q):
        """Return the conjugate of the quaternion.

        :param q: The original quaternion.
        :return: The conjugated quaternion value as an array of 4 elements.
        """
        w, x, y, z = q
        return [w, -x, -y, -z]
