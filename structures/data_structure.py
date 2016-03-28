

class DataStructure(object):
    def __init__(self):
        pass

    def vertex_surrounding(self, vertex_id):
        raise NotImplementedError()

    def elements_with_vertex(self, vertex_id):
        raise NotImplementedError()

    def face_surrounding(self, face_id):
        raise NotImplementedError()

    def switch_triangles(self, face1, face2):
        raise NotImplementedError()

    def mesh_boundary(self):
        raise NotImplementedError()
