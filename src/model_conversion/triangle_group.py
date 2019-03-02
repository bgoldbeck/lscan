# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from src.model_conversion.triangle import Triangle


class TriangleGroup:
    """

    """

    def __init__(self, triangles= None):
        """

        :param triangles: list of Triangles
        """
        if triangles:
            self.triangles = triangles
            self.normal = triangles[0].get_normal()
        else:
            self.triangles = []
            self.normal = None

    def match_normal(self, normal):
        """Checks if the given normal matches the TriangleGroup

        :param normal: [x, y, z]
        :return:
        """
        return (self.normal == normal).all()

    def add_triangle(self, triangle: Triangle):
        """

        :param triangle:
        :return:
        """
        self.triangles.append(triangle)

    def has_neighbor(self, test_triangle: Triangle):
        """
        Checks if given triangle has a neighbor in the triangle group
        :param test_triangle: Triangle
        :return: True or False
        """
        for triangle in self.triangles:
            if Triangle.are_neighbors(triangle, test_triangle):
                return True
        return False

    def rearrange_by_neighbors(self):
        new_triangle_groups = []
        triangles = self.triangles
        if triangles:
            edges = self.triangles[0].edges
            new_triangle_groups.append(triangles[0])
            new_group = TriangleGroup([self.triangles[0]])
            while edges:
                for triangle in triangles:
                    if triangle.has_edge(edges[-1]):
                        pass
            # TODO not complete

    def get_normal(self):
        """
        Returns the normal value
        :return:
        """
        return self.normal

    @staticmethod
    def set_difference(group_1, group_2):
        """
        Returns groups from group_1 that are not in group_2 (group_1 - group_2)
        :param group_1:
        :param group_2:
        :return: list
        """
        return list(set(group_1.triangles) - set(group_2.triangles))