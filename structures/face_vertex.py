from processing.loader import DataLoader
from processing.exceptions import IncorrectFacesException


class FaceVertexStructure():
    def __init__(self, path):
        self.raw_data = DataLoader().load_file(path)
        self.vertex_array = self.raw_data['vertex']
        self.face_array = self.raw_data['face']

    def vertex_neighbors(self):
        temp = []
        result = []
        for i in range(len(self.vertex_array)):
            temp.append(set())
            result.append(set())
        for face in self.face_array:
            for i in range(len(face)):
                temp[face[i]].add(face[(i+1) % len(face)])
                temp[face[i]].add(face[(i+len(face)-1) % len(face)])
        for v in range(len(temp)):
            result[v] |= temp[v]
            for i in temp[v]:
                result[v] |= temp[i]
        return result

    def vertex_faces(self):
        result = []
        for i in range(len(self.vertex_array)):
            result.append(set())
        for i in range(len(self.face_array)):
            for vertex in self.face_array[i]:
                result[vertex].add(i)
        return result

    def face_neighbors(self):
        temp = []
        result = []
        for i in range(len(self.face_array)):
            temp.append(set())
            result.append(set())
        for a in range(len(self.face_array)):
            for b in range(a, len(self.face_array)):
                if a != b and len(set(self.face_array[a]) & set(self.face_array[b])) > 1:
                    temp[a].add(b)
                    temp[b].add(a)
        for i in range(len(self.face_array)):
            result[i] |= temp[i]
            for j in temp[i]:
                result[i] |= temp[j]
        return result

    def triangle_edge_replace(self, face1, face2):
        if face1 == face2 or \
                len(set(self.face_array[face1]) & set(self.face_array[face2])) != 2 or \
                len(self.face_array[face1]) != 3 or \
                len(self.face_array[face2]) != 3:
            raise IncorrectFacesException
        shared_vertexes = list(set(self.face_array[face1]) & set(self.face_array[face2]))
        other_vertexes = list(set(self.face_array[face1]) | set(self.face_array[face2]) - set(shared_vertexes))
        self.face_array[face1] = (other_vertexes[0], other_vertexes[1], shared_vertexes[0])
        self.face_array[face2] = (other_vertexes[0], other_vertexes[1], shared_vertexes[1])

    # TODO
    def mesh_boundary(self):
        pass