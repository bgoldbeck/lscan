import time
from stl import Mesh
from src.util import Util

# Group by normals into N groups
# For each group:recursively find neighbors for all edges
# Copy mesh data array of triangles
# Create a new array to track normals
# Create a new array to store groups


class MeshTriangulation:
    """

    """

    @staticmethod
    def group_mesh_by_normals(triangles_data=Mesh):
        """

        :param triangles_data: Mesh object which contains triangle data from STL file
        :return: array of groups of triangles by normal
        """
        groups = []
        group_match = False
        for pivot in triangles_data:
            for group in groups:
                if (pivot[0] == group[0][0]).all():
                    group_match = True
                    group.append(pivot)
                    break
            if not group_match:
                groups.append([pivot])
            group_match = False
        return groups

    @staticmethod
    def regroup_neighbors(groups):
        """

        :param groups:
        :return: list of new groups of same format
        """
        # TODO: for each group in triangle recursively find neighbor of each triangle to form subgroups
        return groups

    @staticmethod
    def group_triangles_triangulation(mesh=Mesh):
        """

        :param mesh:
        :return:
        """

        group_by_normals = MeshTriangulation.group_mesh_by_normals(mesh.data)
        return MeshTriangulation.regroup_neighbors(group_by_normals)


# test script
start_time = time.time()
mesh = Mesh.from_file(Util.path_conversion("assets/models/plane.stl"))
print(f"normals count: {len(mesh.normals)}")

groups = MeshTriangulation.group_triangles_triangulation(mesh) # return array of triangles grouped together

end_time = time.time()

for idx, val in enumerate(groups):
    print(f"Group {idx + 1}")
    for pos, triangle in enumerate(val):
        print(f"triangle {pos + 1} is : {triangle}")
    print("\n")

print(f"{round(end_time - start_time, 2)} seconds")


# groups is an array of (arrays of (tuples of (array of normal coordinates, array of (arrays of vertices), array of origin)))


