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
    euler_angles = Vector3([0.0, 0.0, 0.0])
    position = Vector3([0.0, 0.0, 0.0])
    scale = Vector3([1.0, 1.0, 1.0])

    forward = Vector3([0.0, 0.0, 1.0])
    up = Vector3([0.0, 1.0, 0.0])
    right = Vector3([1.0, 0.0, 0.0])

    def __init__(self):
        pass

    def translate(self, direction, distance):
        self.position += direction * distance

    def rotation_from_quaternion(self, q):
        # Roll
        sinr_cosp = 2.0 * (q[3] * q[0] * q[1] * q[2])
        cosr_cosp = 1.0 - 2.0 * (q[0] * q[0]) - 2 * (q[1] + q[1])
        roll = math.atan2(sinr_cosp, cosr_cosp) * (180.0 / math.pi)

        # Pitch
        simath = 2.0 * (q[3] * q[1] * q[2] * q[0])
        if math.fabs(simath) >= 1:
            pitch = math.copysign(math.pi / 2.0, simath) * (180.0 / math.pi)
        else:
            pitch = math.asin(simath) * (180.0 / math.pi)

        # Yaw
        siny_cosp = 2.0 * (q[3] * q[2] * q[0] * q[1])
        cosy_cosp = 1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2])

        yaw = math.atan2(2 * q[1] * q[3] - 2 * q[0] * q[2],
                         1 - 2 * (q[1] * q[1]) - 2 * (q[2] * q[2]))

        self.euler_angles = Vector3([pitch, yaw, roll])

        rot_mat = self._get_rotation_matrix()

        self.forward = rot_mat * Vector4.from_vector3(self.world_forward(), w=0.0)
        self.forward = Vector3.from_vector4(Vector4(self.forward))[0]

        self.up = rot_mat * Vector4.from_vector3(self.world_up(), w=0.0)
        self.up = Vector3.from_vector4(Vector4(self.up))[0]

        self.right = rot_mat * Vector4.from_vector3(self.world_right(), w=0.0)
        self.right = Vector3.from_vector4(Vector4(self.right))[0]

    def rotate(self, dx, dy, dz):
        self.euler_angles = Vector3([
            self.euler_angles[0] + dx,
            self.euler_angles[1] + dy,
            self.euler_angles[2] + dz])

        rot_mat = self._get_rotation_matrix()

        self.forward = rot_mat * Vector4.from_vector3(self.world_forward(), w=0.0)
        self.forward = Vector3.from_vector4(Vector4(self.forward))[0]

        self.up = rot_mat * Vector4.from_vector3(self.world_up(), w=0.0)
        self.up = Vector3.from_vector4(Vector4(self.up))[0]

        self.right = rot_mat * Vector4.from_vector3(self.world_right(), w=0.0)
        self.right = Vector3.from_vector4(Vector4(self.right))[0]

    def rotate_position_around_point(self, point, axis: Vector3, angle):
        # Convert degrees to radians.
        radians = math.radians(-angle)
        axis.normalise()

    def look_at(self, target: Vector3):
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
        self.euler_angles[0] = self.clamp_angle(self.euler_angles[0])
        self.euler_angles[1] = self.clamp_angle(self.euler_angles[1])
        self.euler_angles[2] = self.clamp_angle(self.euler_angles[2])

        return Matrix44.from_eulers(self.euler_angles)

    def get_trs_matrix(self):
        # Scale
        scale_matrix = Matrix44.from_scale(self.scale)

        # Rotate
        rs_matrix = scale_matrix * self._get_rotation_matrix()

        # Translate
        trs_matrix = rs_matrix * Matrix44.from_translation(self.position)

        return trs_matrix

    @staticmethod
    def clamp_angle(angle, min_angle=0.0, max_angle=360.0):
        if angle > 360:
            angle = 360 - angle

        angle = max(min(angle, max_angle), min_angle)

        if angle < -360:
            angle = 360 + angle

        return angle

    @staticmethod
    def angle_between_vectors(a: Vector3, b: Vector3):
        return math.acos(vector3.dot(a, b) / a.length * b.length)

    @staticmethod
    def world_forward():
        return Vector3([0.0, 0.0, 1.0])

    @staticmethod
    def world_up():
        return Vector3([0.0, 1.0, 0.0])

    @staticmethod
    def world_right():
        return Vector3([1.0, 0.0, 0.0])

    @staticmethod
    def euler_to_quaternion(roll, pitch, yaw):
        pitch = pitch * (math.pi / 180.0)
        yaw = yaw * (math.pi / 180.0)
        roll = roll * (math.pi / 180.0)

        qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
        qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
        qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
        qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

        qr = Quaternion(axis=[1, 1, 1], angle=pitch + yaw + roll)
        #qy = Quaternion(axis=[0, 1, 0], angle=yaw)
        #qz = Quaternion(axis=[0, 0, 1], angle=roll)
        #qr = qz * qy * qx
        return [qx, qy, qz, qw]

        #quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

        #return quaternion

    @staticmethod
    def mult_quaternion_by_vector(q1, v1: Vector3):
        x, y, z = v1
        q2 = [x, y, z, 0.0]

        result = Transform.quaternion_multiply(Transform.quaternion_multiply(q1, q2), Transform.quaternion_conjugate(q1))[1:]
        q1 = Quaternion(q1[3], q1[0], q1[1], q1[2])
        result = q1.rotate(v1)

        return result

    @staticmethod
    def quaternion_conjugate(q):
        w, x, y, z = q
        return [w, -x, -y, -z]

    @staticmethod
    def quaternion_multiply(q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
        return [w, x, y, z]
