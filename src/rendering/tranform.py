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
from pyrr import *
import math


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
                         1 - 2  * (q[1] * q[1]) - 2 * (q[2] * q[2]))

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

        q_rot = Quaternion.from_axis_rotation(axis, radians)

        translation_matrix = Matrix44.from_translation(point)
        translation_matrix_inverse = Matrix44.from_translation(-point)

        rot_mat = q_rot * translation_matrix_inverse
        rot_mat = translation_matrix * rot_mat

        self.position = rot_mat * Vector4.from_vector3(self.position, w=1.0)
        self.position = Vector3.from_vector4(Vector4(self.position))[0]

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

        qx = Quaternion.from_x_rotation(self.euler_angles[0] * (-math.pi / 180.0))
        qy = Quaternion.from_y_rotation(self.euler_angles[1] * (-math.pi / 180.0))
        qz = Quaternion.from_z_rotation(self.euler_angles[2] * (-math.pi / 180.0))

        return Matrix44.from_quaternion(qz * qy * qx)

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
        while angle < 0.0:
            angle += 360.0

        while angle > 360.0:
            angle -= 360.0

        return max(min(angle, max_angle), min_angle)

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
        pitch = math.radians(pitch)
        yaw = math.radians(yaw)
        roll = math.radians(roll)

        qx = math.sin(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) - math.cos(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        qy = math.cos(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2)
        qz = math.cos(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2) - math.sin(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2)
        qw = math.cos(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        return [qx, qy, qz, qw]

    @staticmethod
    def quaternion_to_euler(quaternion):
        w = quaternion[3]
        x = quaternion[0]
        y = quaternion[1]
        z = quaternion[2]

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        x_out = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        y_out = math.degrees(math.asin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        z_out = math.degrees(math.atan2(t3, t4))

        return [z_out, y_out, x_out]

    def mult_quaternion_by_vector(q, v):
        u = Vector3([q[0], q[1], q[2]])
        s = q[3]

        return (2.0 * Vector3.dot(u, v) * u)\
                 + ((s*s - Vector3.dot(u, u)) * v)\
                 + (2.0 * s * Vector3.cross(u, v))
