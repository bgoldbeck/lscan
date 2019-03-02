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


class UniqueEdgeList:
    """This class is a container for unique edges composed in a list format.
    """

    def __init__(self):
        """Constructor that makes a UniqueEdgeList.
        """
        self.edge_list = []

    def add(self, new_edge: Edge):
        """Add a new edge to this list, but only if it isn't in there already.

        :param new_edge: The new edge to add to the set.
        :return: True, if the new edge was added.
        """
        found = False
        for e in self.edge_list:
            if Edge.are_overlapping_edges(new_edge, e):
                found = True
                break

        if not found:
            self.edge_list.append(new_edge)

        return not found

    @staticmethod
    def set_difference(a, b):
        """This returns a list of edges in set 'a' that aren't in set 'b'.

        :param a: The first set.
        :param b: The second set.
        :return: A list of edges in set 'a' that aren't in set 'b'.
        """
        #result = []
        #for edge_in_a in a:
        #    for edge_in_b in b:
        #        if Edge.same_edge(edge_in_a, edge_in_b):
        #            found = True
        #    if not found:
        #        result.append(edge_in_a)
        #return result
        return list(set(a.edge_list) - set(b.edge_list))


