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


def get_mesh_triangles(mesh: Mesh):
    """
    Converts the mesh to Triangle objects
    :return: List of Triangles
    """
    mesh_triangles = []  # array of Triangles
    for data in mesh.data:
        normal = data[0].round(5)
        vertex_1 = data[1][0]
        vertex_2 = data[1][1]
        vertex_3 = data[1][2]
        edge_1 = Edge(vertex_1[0], vertex_1[1], vertex_1[2], vertex_2[0], vertex_2[1], vertex_2[2])
        edge_2 = Edge(vertex_2[0], vertex_2[1], vertex_2[2], vertex_3[0], vertex_3[1], vertex_3[2])
        edge_3 = Edge(vertex_3[0], vertex_3[1], vertex_3[2], vertex_1[0], vertex_1[1], vertex_1[2])
        mesh_triangles.append(Triangle(edge_1, edge_2, edge_3, normal=normal))
    return mesh_triangles


def make_normal_groups(triangles: []):
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

def make_face(triangle:Triangle, group_triangles: [], bucket: Face):
    """
    For a given triangle recursively finds all the neighbor triangles
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
            bucket = make_face(matching_triangle, group_triangles, bucket)

    return bucket

def make_face_groups(normal_groups: []):
    """
    Regroup triangle groups into groups of triangles that are connected.
    (This is equivalent to grouping into faces)
    :param triangles_groups: List of TriangleGroups
    :return: List of faces
    """
    all_faces = []  # List of faces
    for group in normal_groups:
        # Create a bucket of a Face with first triangle in the group
        # Recursively add all neighboring triangles to that bucket
        while group:
            triangle = group.pop(0)
            bucket = Face([triangle])
            bucket = make_face(triangle, group, bucket)  # Recursively find neighbor of a triangle
            group = Face.set_difference(group, bucket.triangles)  # Finding remaining triangles to find neighbors
            all_faces.append(bucket)
    return all_faces

def make_face_boundaries(faces: []):
    """Step 2. Remove shared edges.
    :param faces: List of faces.
    :return: List of a list of edges where each list of edges is the edges that
    were not shared in that face.
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

def make_simple_outlines(grouped_edges):
    """
    #Step 3
    :param grouped_edges: A list of list of edges, grouped by connectivity between edges.
    :return: List of a list of edges where each list of edges have been simplified. Connecting
    edges that were parallel are joined together.
    """
    output = []
    k = -1
    for outline_edge_group in grouped_edges:
        make_simple_boundary(outline_edge_group)
        k += 1
        output.append(UniqueEdgeList())
        output[k] = outline_edge_group
    return output

def make_simple_boundary(outline_edge_group: UniqueEdgeList):
    """
    Step 3 recursive
    :param outline_edge_group: A list of edges, grouped by connectivity between edges.
    :return: ???
    """
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
                    make_simple_boundary(outline_edge_group)


def split_boundaries(grouped_edges):
    """
    Step 3 part 2
    Splits each outline into groups by connectivity. If a face has holes, its
    outline would be split into multiple groups
    :param grouped_edges: A list of UniqueEdgeLists that compose the edges of a face.
    :return:
    """
    buckets = []

    for group in grouped_edges:
        if len(group.edge_list) > 0:
            current_edge_list = UniqueEdgeList()
            current_edge_list.add(group.edge_list[0])

            unique_edge_lists = split_boundary([current_edge_list], group, 0)

            buckets.append(unique_edge_lists)

    return buckets

def split_boundary(unique_edge_lists: [], all_edges: UniqueEdgeList, i: int):
    """
    Step 3 part 2 recursive
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
                    return split_boundary(unique_edge_lists, all_edges, i)

    if len(all_edges.edge_list) > 0:
        new_edge_list = UniqueEdgeList()
        new_edge_list.add(all_edges.edge_list[0])
        unique_edge_lists.append(new_edge_list)

        return split_boundary(unique_edge_lists, all_edges, i + 1)
    return split_boundary(unique_edge_lists, all_edges, i)


def find_outside_boundary(buckets):
    """
    find_outside_boundary (put outside outline at index 0)
    :param grouped_edges:
    :return:
    """
    # output_step_3_part_3: Contains a list of "buckets", where each bucket contains a list of

    for bucket in buckets:
        outer_boundary_index = 0
        max_dist_to_origin = -1.0
        for i in range(len(bucket)):
            boundary = bucket[i]
            for edge in boundary.edge_list:
                origin_to_start = Edge(0, 0, 0, edge.x1, edge.y1, edge.z1)
                origin_to_end = Edge(0, 0, 0, edge.x2, edge.y2, edge.z2)

                if origin_to_start.length() > max_dist_to_origin:
                    max_dist_to_origin = origin_to_start.length()
                    outer_boundary_index = i

                if origin_to_end.length() > max_dist_to_origin:
                    max_dist_to_origin = origin_to_end.length()
                    outer_boundary_index = i

        if outer_boundary_index > 0:
            # Swap list[outer_boundary_index] and list[0]
            bucket[outer_boundary_index], bucket[0] = bucket[0], bucket[outer_boundary_index]

    return buckets