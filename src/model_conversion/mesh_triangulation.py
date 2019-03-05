# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import matplotlib.pyplot as plt
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
            normal = data[0].round(5)
            vertex_1 = data[1][0]
            vertex_2 = data[1][1]
            vertex_3 = data[1][2]
            edge_1 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_2[0], vertex_2[1], vertex_2[2])
            edge_2 = Edge(vertex_2[0], vertex_2[1], vertex_2[2], vertex_3[0], vertex_3[1], vertex_3[2])
            edge_3 = Edge(vertex_3[0], vertex_3[1], vertex_3[2], vertex_1[0], vertex_1[1], vertex_1[2])
            mesh_triangles.append(Triangle(edge_1, edge_2, edge_3, normal=normal))
        return mesh_triangles

    def group_triangles_triangulation(self):
        """
        This method converts the mesh into a list of Faces. A Face has list of neighbor Triangles with same normal
        :return: List of Face
        """
        triangles = self.get_mesh_triangles()
        groups = MeshTriangulation.group_triangles_by_normals(triangles)
        return MeshTriangulation.regroup_by_neighbors(groups)

    def step_2(self, faces: []):
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
            shared_edges = UniqueEdgeList()
            # len(face.triangles) should return the # of triangles in the face.
            for m in range(len(face.triangles)):
                for n in range(len(face.triangles)):
                    if m is not n:
                        for i in range(3):
                            for j in range(3):
                                # Compare an edge in triangle "m" vs the 3 other edges in
                                # triangle "n"
                                if Edge.are_overlapping_edges(face.triangles[m].edges[i],
                                                              face.triangles[n].edges[j]):
                                    shared_edges.add(face.triangles[m].edges[i])

            k += 1
            output.append(UniqueEdgeList())
            all_edges_in_face = face.get_edges()
            output[k] = UniqueEdgeList.set_difference(all_edges_in_face, shared_edges)

        return output

    def step_3(self, grouped_edges):
        """
        :param grouped_edges: A list of list of edges, grouped by connectivity between edges.
        :return: List of a list of edges where each list of edges have been simplified. Connecting
        edges that were parallel are joined together.
        """
        output = []
        k = -1
        for outline_edge_group in grouped_edges:
            self._step_3_recursive(outline_edge_group)
            k += 1
            output.append(UniqueEdgeList())
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
                            Edge(start_vertex[0], start_vertex[1], start_vertex[2],  # Edge Start
                                 end_vertex[0], end_vertex[1], end_vertex[2]))  # Edge end
                        self._step_3_recursive(outline_edge_group)

    def step_3_part_2(self, grouped_edges):
        """

        :param grouped_edges: A list of UniqueEdgeLists that compose the edges of a face.
        :return:
        """
        buckets = []

        for group in grouped_edges:
            if len(group.edge_list) > 0:
                current_edge_list = UniqueEdgeList()
                current_edge_list.add(group.edge_list[0])

                unique_edge_lists = self._step_3_part_2_recursive([current_edge_list], group, 0)

                buckets.append(unique_edge_lists)

        return buckets

    def _step_3_part_2_recursive(self, unique_edge_lists: [], all_edges: UniqueEdgeList, i: int):
        """

        :param all_edges:
        :return:
        """
        if len(all_edges.edge_list) == 0:
            return unique_edge_lists

        # Remove all_edges from list that exist in bucket.
        for e in unique_edge_lists[i].edge_list:
            all_edges.remove(e)

        for e in all_edges.edge_list:
            for current_edge in unique_edge_lists[i].edge_list:
                if (not Edge.same_edge(e, current_edge)) and \
                        (Edge.has_shared_vertex(e, current_edge) is not None):
                    if unique_edge_lists[i].add(e):
                        return self._step_3_part_2_recursive(unique_edge_lists, all_edges, i)

        if len(all_edges.edge_list) > 0:
            new_edge_list = UniqueEdgeList()
            new_edge_list.add(all_edges.edge_list[0])
            unique_edge_lists.append(new_edge_list)

            return self._step_3_part_2_recursive(unique_edge_lists, all_edges, i + 1)
        return self._step_3_part_2_recursive(unique_edge_lists, all_edges, i)

    def step_3_part_3(self, grouped_edges):
        """

        :param grouped_edges:
        :return:
        """
        list_of_outer_boundary_indices = []

        for bucket in grouped_edges:
            outer_boundary_index = 0
            max_dist_to_origin = -1.0
            for i in range(len(bucket)):
                for edge in bucket[i].edge_list:
                    origin_to_start = Edge(0, 0, 0, edge.x1, edge.y1, edge.z1)
                    origin_to_end = Edge(0, 0, 0, edge.x2, edge.y2, edge.z2)

                    if origin_to_start.length() > max_dist_to_origin:
                        max_dist_to_origin = origin_to_start.length()
                        outer_boundary_index = i

                    if origin_to_end.length() > max_dist_to_origin:
                        max_dist_to_origin = origin_to_end.length()
                        outer_boundary_index = i

            list_of_outer_boundary_indices.append(outer_boundary_index)

        return list_of_outer_boundary_indices

    @staticmethod
    def group_triangles_by_normals(triangles):
        """
        Group triangles by normal
        :param triangles: List of Triangles
        :return: List of List of Triangles
        """
        triangles_groups = []
        group_match = False
        for triangle in triangles:
            for group in triangles_groups:
                if (group[0].normal == triangle.normal).all():
                    group_match = True
                    group.append(triangle)
                    break
            if not group_match:
                triangles_groups.append([triangle])
            group_match = False
        return triangles_groups

    @staticmethod
    def regroup_by_neighbors(triangles_groups):
        """
        Regroup triangle groups by neighbors
        :param triangles_groups: List of TriangleGroups
        :return:
        """
        all_faces = []  # List of faces
        for group in triangles_groups:
            # Create a bucket of a Face with first triangle in the group
            # Recursively add all neighboring triangles to that bucket
            while group:
                triangle = group.pop(0)
                bucket = Face([triangle])
                bucket = MeshTriangulation.regroup(triangle, group, bucket)  # Recursively find neighbor of a triangle
                group = Face.set_difference(group, bucket.triangles)  # Finding remaining triangles to find neighbors
                all_faces.append(bucket)
        return all_faces

    @staticmethod
    def regroup(triangle, group_triangles, bucket):
        """

        :param triangle: Find neighbors of this triangle
        :param group_triangles: List of remaining triangles in the group
        :param bucket: A Face object to hold neighbor triangles
        :return: A bucket(Face object) which contains list of neighbor triangles
        """
        # Base Case : group_triangles == [] , group_triangles == None
        if not group_triangles:
            return bucket

        edges = triangle.edges # Edges of the triangle

        # Find a triangle with matching edges and add to the bucket
        for edge in edges:
            matching_triangle_index = Triangle.match_triangle_index(edge, group_triangles)
            if matching_triangle_index is not None:
                matching_triangle = group_triangles.pop(matching_triangle_index)
                bucket.add_triangle(matching_triangle)
                bucket = MeshTriangulation.regroup(matching_triangle, group_triangles, bucket)

        return bucket


# test script

# mesh = Mesh.from_file(Util.path_conversion("assets/models/3001.stl"), calculate_normals=False)
# print(f"Total Triangle count: {len(mesh.normals)}")
# mesh_triangulation = MeshTriangulation(mesh)
# groups = mesh_triangulation.group_triangles_triangulation()
# print(f"Groups {len(groups)}")
# total_triangles_group = 0
# for index, group in enumerate(groups):
#     print(f"Group {index + 1} has {len(group.triangles)} triangles")
#     total_triangles_group += len(group.triangles)
# print(f"Total triangles in groups: {total_triangles_group}")

