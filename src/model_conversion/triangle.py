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
from src.model_conversion.edge import Edge


class Triangle:
    """A triangle is a set of 3 edges.
    """
    def __init__(self, e1, e2, e3, normal=None):
        """Build a triangle from three edges.

        :param e1: The first edge.
        :param e2: The second edge.
        :param e3: The third edge.
        """
        self.edges = [e1, e2, e3]
        self.normal = normal

    def is_closed_loop(self):
        """Determine if a triangle has all its edges connected.

        :return: True, if all it's edges are connected.
        """
        start_edge = self.edges[0]

        first_check = Edge.has_shared_vertex(start_edge, self.edges[1])
        second_check = Edge.has_shared_vertex(start_edge, self.edges[2])
        third_check = Edge.has_shared_vertex(self.edges[1], self.edges[2])

        return first_check and second_check and third_check

    def get_normal(self):
        """Get the normal of the face
        :return:
        """
        return self.normal

    def has_edge(self, check_edge):
        """
        Checks if the triangle has the matching
        :param check_edge: Edge
        :return: True or False
        """
        for edge in self.edges:
            if Edge.are_overlapping_edges(edge, check_edge):
                return True
        return False

    def get_first_edge(self):
        """"
        Get first edge in the triangle:
        :return edges[0] : edge 1.
        """
        return self.edges[0]

    def get_second_edge(self):
        """"
        Get second edge in the triangle:
        :return edges[1] : edge 2.
        """
        return self.edges[1]

    def get_third_edge(self):
        """"
        Get third edge in the triangle:
        :return edges[2] : edge 3.
        """
        return self.edges[2]

    @staticmethod
    def are_neighbors(t1, t2):
        """Determine if two triangles have a shared edge.

        :param t1: The first triangle.
        :param t2: The second triangle.
        :return: True, if the triangles had a shared edge.
        """
        result = False
        # x being an edge in the first triangle.
        for x in t1:
            # y being an edge in the second triangle.
            for y in t2:
                if Edge.same_edge(x, y):
                    # We just need one shared edge to be true.
                    result = True
        return result

    @staticmethod
    def are_equal(t1, t2):
        """
        Determine if two triangles are equal
        :param t1: Triangle
        :param t2: Triangle
        :return: True if all edges overlaps
        """
        pass

    @staticmethod
    def match_triangle_index(edge: Edge, triangles):
        """
        Checks if an any triangle has a matching edge or not
        :param edge: An Edge to check for matching traingle
        :param triangles: List of Triangles
        :return: An index of matching triangle or None
        """
        for index, triangle in enumerate(triangles):
            if triangle.has_edge(edge):
                return index
        return None
