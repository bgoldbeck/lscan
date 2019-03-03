# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import time
from stl import Mesh
from src.model_conversion.edge import Edge
from src.model_conversion.unique_edge_list import UniqueEdgeList
from src.model_conversion.triangle import Triangle
from src.util import Util
from src.model_conversion.face import Face

# Group by normals into N groups
# For each group:recursively find neighbors for all edges
# Copy mesh data array of triangles
# Create a new array to track normals
# Create a new array to store groups


class MeshTriangulation:
    """

    """

    def __init__(self, mesh: Mesh):
        self.mesh = mesh

    def run(self):
        # Step 1
        output_from_step_1 = self.group_triangles_triangulation()
        # Step 2
        self._step_2(output_from_step_1)
        # Step 3
        # Step 4

    def get_mesh_triangles(self):
        """
        Converts the mesh to Triangle objects
        :return: List of Triangles
        """
        mesh_triangles = []  # array of Triangles
        for data in self.mesh.data:
            normal = data[0]
            vertex_1 = data[1][0]
            vertex_2 = data[1][1]
            vertex_3 = data[1][2]
            edge_1 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_2[0], vertex_2[1], vertex_2[2])
            edge_2 = Edge(vertex_2[0], vertex_2[1], vertex_2[2], vertex_3[0], vertex_3[1], vertex_3[2])
            edge_3 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_3[0], vertex_3[1], vertex_3[2])
            mesh_triangles.append(Triangle(edge_1, edge_2, edge_3, normal=normal))
        return mesh_triangles

    def group_triangles_triangulation(self):
        """

        :return:
        """
        triangles = self.get_mesh_triangles()
        groups = MeshTriangulation.group_triangles_by_normals(triangles)
        return MeshTriangulation.regroup_by_neighbors(groups) # goes infinite loop

    def _step_2(self, faces):
        """Step 2. Remove shared edges.
        Input: List of faces.
        Output: List of a list of edges where each list of edges is the edges that were not shared
        in that face.
        :return:
        """
        # Faces is a list of faces, where faces are composed of triangles on the same plane and
        # have some edge connecting them.
        # faces.count() should return the number of planes on an object IE: A cube has 6 faces.
        output = []
        k = -1
        for face in faces:
            k += 1
            output[k] = UniqueEdgeList()
            # face.count() should return the # of triangles in the face.
            for m in range(face.count()):
                for n in range(face.count()):
                    if m is not n:
                        for i in range(3):
                            j = i + 1
                            if i is 2:
                                j = 0
                            # Compare an edge in triangle "m" vs the 3 other edges in
                            # triangle "n"
                            tri1_edge = Edge(
                                face[m, i, 0], face[m, i, 1], face[m, i, 2],
                                face[m, j, 0], face[m, j, 1], face[m, j, 2])

                            tri2_edge01 = Edge(
                                face[n, 0, 0], face[n, 0, 1], face[n, 0, 2],
                                face[n, 1, 0], face[n, 1, 1], face[n, 1, 2])

                            tri2_edge12 = Edge(
                                face[n, 1, 0], face[n, 1, 1], face[n, 1, 2],
                                face[n, 2, 0], face[n, 2, 1], face[n, 2, 2])

                            tri2_edge20 = Edge(
                                face[n, 2, 0], face[n, 2, 1], face[n, 2, 2],
                                face[n, 0, 0], face[n, 0, 1], face[n, 0, 2])

                            if Edge.are_overlapping_edges(tri1_edge, tri2_edge01):
                                output[k].Add(tri1_edge)

                            if Edge.are_overlapping_edges(tri1_edge, tri2_edge12):
                                output[k].Add(tri1_edge)

                            if Edge.are_overlapping_edges(tri1_edge, tri2_edge20):
                                output[k].Add(tri1_edge)

            output[k] = UniqueEdgeList.set_difference(face.to_edge_list(), output[k])

        return output

    def _step_3(self, grouped_edges):
        """
        :param grouped_edges: A list of list of edges, grouped by connectivity between edges.
        :return: List of a list of edges where each list of edges have been simplified. Connecting
        edges that were parallel are joined together.
        """
        output = []
        k = -1
        for outline_edge_group in grouped_edges:
            k += 1
            self._step_3_recursive(outline_edge_group)
            # Assuming outline_edge_group is changed by step_3_recursive.
            output[k] = outline_edge_group
        return output

    def _step_3_recursive(self, outline_edge_group: UniqueEdgeList):
        for edge_outer in outline_edge_group.edge_list:
            for edge_inner in outline_edge_group.edge_list:
                if not Edge.same_edge(edge_inner, edge_outer):
                    shared_vertex = Edge.has_shared_vertex(edge_inner, edge_outer)
                    parallel = Edge.are_parallel_or_anti_parallel(edge_inner, edge_outer)
                    if shared_vertex is not None and parallel:
                        # Case 1.
                        start_vertex = [edge_inner.x1, edge_inner.y1, edge_inner.z1]

                        # Case 2.
                        if (edge_inner.x1 == shared_vertex[0] and
                            edge_inner.y1 == shared_vertex[1] and
                            edge_inner.z1 == shared_vertex[2]):
                                start_vertex = [edge_inner.x2, edge_inner.y2, edge_inner.z2]

                        # Case 3.
                        end_vertex = [edge_outer.x1, edge_outer.y1, edge_outer.z1]

                        # Case 4.
                        if (edge_outer.x1 == shared_vertex[0] and
                            edge_outer.y1 == shared_vertex[1] and
                            edge_outer.z1 == shared_vertex[2]):
                                end_vertex = [edge_outer.x2, edge_outer.y2, edge_outer.z2]
                        outline_edge_group.edge_list.remove(edge_outer)
                        outline_edge_group.edge_list.remove(edge_inner)
                        outline_edge_group.add(
                            Edge(start_vertex[0], start_vertex[1], start_vertex[2], # Edge Start
                                 end_vertex[0], end_vertex[1], end_vertex[2]))  # Edge end
                        self._step_3(outline_edge_group)

    def _step_3_part_2(self, grouped_edges):
        """

        :param grouped_edges: A list of list of edges that compose the edges of faces.
        :return:
        """
        grouped_buckets = []

        for group in grouped_edges:
            first_bucket = UniqueEdgeList()
            first_bucket.add(grouped_edges.edgeList[0])
            buckets = [first_bucket]
            buckets = self._step_3_part_2_recursive(buckets, group, 0)
            grouped_buckets.append(buckets)

        return grouped_buckets

    def _step_3_part_2_recursive(self, buckets, edges, i):
        """

        :param edges:
        :return:
        """
        if edges.edge_list.count() == 0:
            return buckets

        bucket = buckets[i]

        for edge in edges.edge_list:
            for edge_in_bucket in bucket.edge_list:
                if not (Edge.same_edge(edge, edge_in_bucket) and
                        Edge.has_shared_vertex(edge, edge_in_bucket)):
                    if bucket.add(edge):
                        return self._step_3_part_2_recursive(buckets, edges, i)

        # Remove edges from list that exist in bucket.
        for edge in bucket.edge_list:
            edges.edge_list.remove(edge)

        if edges.edge_list.count() > 0:
            new_bucket = UniqueEdgeList()
            new_bucket.add(edges.edge_list[0])
            buckets.add(new_bucket)
            return self._step_3_part_2_recursive(buckets, edges, i + 1)
        return self._step_3_part_2_recursive(buckets, edges, i)

    def _step_3_part_3(self, grouped_edges):
        """

        :param grouped_edges:
        :return:
        """
        max_dist_to_origin = -1.0
        outer_boundary_index = 0

    @staticmethod
    def group_triangles_by_normals(triangles):
        """
        Group triangles by normal
        :param triangles: List of Triangles
        :return: List of Faces
        """
        faces_groups = []
        group_match = False
        for triangle in triangles:
            for group in faces_groups:
                if group.match_normal(triangle.normal):
                    group_match = True
                    group.add_triangle(triangle)
                    break
            if not group_match:
                faces_groups.append(Face([triangle]))
            group_match = False
        return faces_groups

    @staticmethod
    def regroup_by_neighbors(groups):
        """
        regroup by neighbors
        :param groups: List of TriangleGroups
        :return:
        """
        all_groups = []
        for group in groups:
            group_triangles = group.triangles
            triangle = group_triangles.pop(-1)
            while group_triangles:
                new_group = MeshTriangulation.regroup(triangle, group_triangles)
                all_groups.append(new_group)
        return all_groups

    @staticmethod
    def regroup(triangle, group_triangles):
        """
        Recursive method
        :param group:
        :return:
        """
        if not group_triangles:
            return []
        edges = triangle.edges
        match_triangles_1 = Triangle.get_edge_match(edges[0], group_triangles)
        if not match_triangles_1:
            return []
        edge_1 = MeshTriangulation.regroup(match_triangles_1, group_triangles).append(match_triangles_1)
        match_triangles_2 = Triangle.get_edge_match(edges[1], group_triangles)
        if not match_triangles_2:
            return []
        edge_2 = MeshTriangulation.regroup(match_triangles_2, group_triangles).append(match_triangles_2)
        match_triangles_3 = Triangle.get_edge_match(edges[2], group_triangles)
        if not match_triangles_3:
            return []
        edge_3 = MeshTriangulation.regroup(match_triangles_3, group_triangles).append(match_triangles_3)
        return edge_1 + edge_2 + edge_3
# test script

start_time = time.time()
mesh = Mesh.from_file(Util.path_conversion("assets/models/cube.stl"), calculate_normals=False)
mesh_trianglulation = MeshTriangulation(mesh)
group = mesh_trianglulation.group_triangles_triangulation()
end_time = time.time()
print(len(group))
print(f"Triangles count: {len(mesh.normals)}")
print(end_time - start_time)


