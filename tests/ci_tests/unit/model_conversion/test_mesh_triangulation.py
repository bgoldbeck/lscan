# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import unittest
import math
from stl import Mesh
from src.util import Util
import matplotlib.pyplot as plt
from src.model_conversion.edge import Edge
import src.model_conversion.mesh_triangulation as MeshTriangulation
from src.model_conversion.face import Face
from src.model_conversion.triangle import Triangle


class TestMeshTriangulation(unittest.TestCase):

    def test_mesh_tris(self):
        # Load mesh
        mesh = Mesh.from_file(Util.path_conversion("assets/models/2_holes.stl"),
                              calculate_normals=False)

        # Create list of triangle objects from mesh
        triangles = MeshTriangulation.get_mesh_triangles(mesh)
        print("Found " + str(len(triangles)) + " triangle(s).")

        # Group triangles by their normals
        normal_groups = MeshTriangulation.make_normal_groups(triangles)
        print("Found " + str(len(normal_groups)) + " normal group(s).")

        # Group normal groups into faces (by connected parts)
        faces = MeshTriangulation.make_face_groups(normal_groups)
        print("Found " + str(len(faces)) + " face(s).")

        # Get only outline edges for each face
        face_outlines = MeshTriangulation.make_face_boundaries(faces)
        for i in range(len(face_outlines)):
            print("Face #" + str(i) + ": Found " + str(len(face_outlines[i].edge_list))
                  + " edges in outline.")

        # Simplify outline edges for each face (remove redundant vertices)
        simple_outlines = MeshTriangulation.make_simple_outlines(face_outlines)
        for i in range(len(simple_outlines)):
            print("Face #" + str(i) + ": Found " + str(len(simple_outlines[i].edge_list))
                  + " edges in simplified outline.")

        # Split each outline by connected parts
        separate_outlines = MeshTriangulation.split_boundaries(simple_outlines)
        for i in range(len(separate_outlines)):
            num_outlines = len(separate_outlines[i])
            print("Face #" + str(i) + ": Found " + str(num_outlines)
                  + " separate outline(s)")
            for j in range(num_outlines):
                print("\tOutline #" + str(j) + ": Found "
                      + str(len(separate_outlines[i][j].edge_list))
                      + " edges.")

        ordered_separate_outlines = MeshTriangulation.find_outside_boundary(separate_outlines)

        t = -1
        print(f"Length of output_step_3_part_2: " + str(
            len(ordered_separate_outlines)))

        for i in range(len(ordered_separate_outlines)):
            bucket = ordered_separate_outlines[i]
            # print(f"Outer Boundary Index: " + str(output_step_3_part_3[i]))
            colors = ['g', 'b', 'k', 'y', 'r']
            for boundary in bucket:
                t += 1
                if t > 4:
                    t = 0
                for edge in boundary.edge_list:
                    plt.plot([edge.x1, edge.x2], [edge.y1, edge.y2], marker="o",
                             color=colors[t])
            plt.show()




        # faces = self.group_triangles_triangulation()
        # Step 2
        # self._step_2(output_from_step_1)
        # Step 3
        # Step 4

        """# test script

        # start_time = time.time()
        mesh = Mesh.from_file(Util.path_conversion("assets/models/2_holes.stl"), calculate_normals=False)
        mesh_triangulation = MeshTriangulation(mesh)
        # group = mesh_trianglulation.group_triangles_triangulation()
        # end_time = time.time()

        # print(len(group))
        print(f"Triangles count: {len(mesh.normals)}")
        # print(end_time - start_time)

        output_step_1 = mesh_triangulation.group_triangles_triangulation()

        output_step_2 = mesh_triangulation.make_face_boundaries(output_step_1)

        output_step_3 = mesh_triangulation.make_simple_outlines(output_step_2)

        output_step_3_part_2 = mesh_triangulation.split_boundaries(output_step_3)

        output_step_3_part_3 = mesh_triangulation.find_outside_boundary(output_step_3_part_2)

        # output_step_3_part_3: Contains a list of "buckets", where each bucket contains a list of
        # UniqueEdgeLists. Inside each "bucket", the boundary at index zero is the outer most boundary.

        print(f"Triangles count: {len(mesh.normals)}")

        t = -1
        print(f"Length of output_step_3_part_2: " + str(len(output_step_3_part_3)))

        for i in range(len(output_step_3_part_3)):
            bucket = output_step_3_part_3[i]
            print(f"Length of bucket: " + str(len(bucket)))
            #print(f"Outer Boundary Index: " + str(output_step_3_part_3[i]))
            colors = ['g', 'b', 'k', 'y', 'r']
            for boundary in bucket:
                t += 1
                if t > 4:
                    t = 0
                print(f"col index: " + str(t))
                for edge in boundary.edge_list:
                    plt.plot([edge.x1, edge.x2], [edge.y1, edge.y2], marker="o", color=colors[t])
            plt.show()"""
