from processing.loader import DataLoader
from processing.exceptions import IncorrectFacesException
from data_structure import DataStructure


class FaceVertexStructure(DataStructure):
    def __init__(self, path):
        self.raw_data = DataLoader().load_file(path)
        self.vertex_array = self.raw_data['vertex']
        self.face_array = self.raw_data['face']

    def __vertex_neighbors(self, vertex_id):
        faces = self.elements_with_vertex(vertex_id)
        result = set()
        for face in faces:
            result.add(face[(face.index(vertex_id) + 1 + len(face)) % len(face)])
            result.add(face[(face.index(vertex_id) - 1 + len(face)) % len(face)])
        return result

    def vertex_surrounding(self, vertex_id):
        temp = self.__vertex_neighbors(vertex_id)
        result = set()
        result = result.union(temp)
        for v in temp:
            result = result.union(self.__vertex_neighbors(v))
        return list(result)

    def elements_with_vertex(self, vertex_id):
        result = []
        for i in self.face_array:
            if vertex_id in i:
                result.append(i)
        return result

    def __face_neighbors(self, face_id):
        result = set()
        face = self.face_array[face_id]
        for f in range(len(self.face_array)):
            if face != self.face_array[f] and len(set(face) & set(self.face_array[f])) > 1:
                result.add(f)
        return result

    def face_surrounding(self, face_id):
        result = set()
        temp = self.__face_neighbors(face_id)
        result = result.union(temp)
        for f in temp:
            result = result.union(self.__face_neighbors(f))
        return list(result)

    def switch_triangles(self, face1, face2):
        if face1 == face2 or \
                len(set(self.face_array[face1]) & set(self.face_array[face2])) != 2 or \
                len(self.face_array[face1]) != 3 or \
                len(self.face_array[face2]) != 3:
            raise IncorrectFacesException
        shared_vertexes = list(set(self.face_array[face1]) & set(self.face_array[face2]))
        other_vertexes = list(set(self.face_array[face1]) | set(self.face_array[face2]) - set(shared_vertexes))
        self.face_array[face1] = (other_vertexes[0], other_vertexes[1], shared_vertexes[0])
        self.face_array[face2] = (other_vertexes[0], other_vertexes[1], shared_vertexes[1])

    def mesh_boundary(self):
        for v in range(len(self.vertex_array)):
            if len(self.__vertex_neighbors(v)) < 2:
                return False
        return True