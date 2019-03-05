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
from src.model_conversion.mesh_triangulation import MeshTriangulation
from src.model_conversion.face import Face
from src.model_conversion.triangle import Triangle


class TestMeshTriangulation(unittest.TestCase):

    def test_mesh_tris(self):
        # test script

        # start_time = time.time()
        mesh = Mesh.from_file(Util.path_conversion("assets/models/2_holes.stl"), calculate_normals=False)
        mesh_triangulation = MeshTriangulation(mesh)
        # group = mesh_trianglulation.group_triangles_triangulation()
        # end_time = time.time()

        # print(len(group))
        print(f"Triangles count: {len(mesh.normals)}")
        # print(end_time - start_time)

        output_step_1 = mesh_triangulation.group_triangles_triangulation()

        output_step_2 = mesh_triangulation.step_2(output_step_1)

        output_step_3 = mesh_triangulation.step_3(output_step_2)

        output_step_3_part_2 = mesh_triangulation.step_3_part_2(output_step_3)

        output_step_3_part_3 = mesh_triangulation.step_3_part_3(output_step_3_part_2)

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
            plt.show()
