# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from stl import Mesh
from src.model_conversion.edge import Edge
from src.model_conversion.triangle import Triangle
from src.util import Util
from src.model_conversion.triangle_group import TriangleGroup

# Group by normals into N groups
# For each group:recursively find neighbors for all edges
# Copy mesh data array of triangles
# Create a new array to track normals
# Create a new array to store groups


class MeshTriangulation:
    """

    """

    @staticmethod
    def group_triangles_by_normals(triangles):
        groups = [] # array of TriangleGroup
        group_match = False
        for triangle in triangles:
            for group in groups:
                if group.match_normal(triangle.normal):
                    group_match = True
                    group.add_triangle(triangle)
                    break
            if not group_match:
                groups.append(TriangleGroup([triangle]))
            group_match = False
        return groups

    @staticmethod
    def regroup_by_neighbors(groups):
        """
        regroup by neighbors
        :param groups: List of TriangleGroups
        :return:
        """
        new_group = []
        for group in groups:
            new_group.append(group.rearrange_by_neighbors())
        return new_group

    @staticmethod
    def group_triangles(triangles):
        groups = MeshTriangulation.group_triangles_by_normals(triangles)
        return MeshTriangulation.regroup_by_neighbors(groups)




# test script


mesh = Mesh.from_file(Util.path_conversion("assets/models/cube.stl"), calculate_normals=False)
print(f"Triangles count: {len(mesh.normals)}")
mesh_triangles = []  # array of Triangles
for data in mesh.data:
    normal = data[0]
    vertex_1 = data[1][0]
    vertex_2 = data[1][1]
    vertex_3 = data[1][2]
    edge_1 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_2[0], vertex_2[1], vertex_2[2])
    edge_2 = Edge(vertex_2[0], vertex_2[1], vertex_2[2], vertex_3[0], vertex_3[1], vertex_3[2])
    edge_3 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_3[0], vertex_3[1], vertex_3[2])
    mesh_triangles.append(Triangle(edge_1, edge_2, edge_3, normal=normal))

# return array of TriangleGroups [TriangleGroup, TriangleGroup, ...]
groups = MeshTriangulation.group_triangles(mesh_triangles)
for group in groups:
    print(group)



