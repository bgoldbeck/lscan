# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import unittest, math
from src.model_conversion.edge import Edge


class EdgeTest(unittest.TestCase):

    def test_EdgeIsLengthIsSqrtThree(self):
        test_edge = Edge(0, 0, 0, 1, 1, 1)
        length = test_edge.length()
        self.assertTrue(length, math.sqrt(3))

    def test_EdgeDot(self):
        test_edge1 = Edge(0, 0, 0, 1, 1, 1)
        test_edge2 = Edge(1, 1, 1, 0, 0, 0)
        test_edge3 = Edge(-1, -1, -1, 0, 0, 0)
        dot1 = Edge.dot(test_edge1, test_edge2)
        dot2 = Edge.dot(test_edge1, test_edge3)
        self.assertEqual(dot1, -3)
        self.assertEqual(dot2, 3)

    def test_EdgeSameEdge(self):
        test_edge1 = Edge(0, 0, 0, 1, 1, 1)
        test_edge2 = Edge(1, 1, 1, 0, 0, 0)
        test_edge3 = Edge(0, 0, 0, 2, 2, 2)

        same_edge1 = Edge.same_edge(test_edge1, test_edge2)
        same_edge2 = Edge.same_edge(test_edge1, test_edge1)
        same_edge3 = Edge.same_edge(test_edge1, test_edge3)
        self.assertFalse(same_edge1)
        self.assertTrue(same_edge2)
        self.assertFalse(same_edge3)

    # TODO
    def test_AreOverlappingEdges(self):
        test_edge1 = Edge(0, 0, 0, 1, 1, 1)
        test_edge2 = Edge(1, 1, 1, 0, 0, 0)
        pass

    # TODO
    def test_HasSharedVertex(self):
        pass

    # TODO
    def test_EdgeIsParallelOrAntiparallel(self):
        test_edge1 = Edge(0, 0, 0, 1, 1,1)
        test_edge_parallel = Edge(1, 1, 1, 2, 2, 2)
        test_edge_anti_parallel = Edge(2, 2, 2, 1, 1, 1)

        pass


