from processing.loader import DataLoader
from structures.data_structure import DataStructure


class HalfEdge(object):
    def __init__(self, vertex=None, pair=None, face=None, next_edge=None):
        self.vertex = vertex
        self.pair = pair
        self.face = face
        self.next_edge = next_edge
        self.prev_edge = None
        self.number = None

    def __str__(self):
        return 'Egde: vertex %s' % (self.vertex)


class HEVertex(object):
    def __init__(self, coordinate, edge=None):
        self.coordinate = coordinate
        self.edge = edge

    def __str__(self):
        return '(%f, %f, %f)' % (self.coordinate[0], self.coordinate[1],
                                 self.coordinate[2])


class HEFace(object):
    def __init__(self, edge):
        self.edge = edge


class HalfEdgeStructure(DataStructure):
    def __init__(self, vertex, edge, face):
        self.half_edges = {}
        self.vertices = []
        self.faces = []
        self.__build_structure(vertex, edge, face)

    def __build_structure(self, vertices, edges, faces, ccw=True):
        for idx, vertex in enumerate(vertices):
            self.vertices.append(HEVertex(vertex))

        for idx, face in enumerate(faces):

            edges = [(face[i], face[(i+1) % len(face)]) for i in xrange(len(face))]

            for e in xrange(len(edges)):
                edge = edges[e]
                next_edge = edges[(e + 1) % len(edges)]
                pair = (edge[1], edge[0])
                if edge not in self.half_edges.keys():
                    self.half_edges[edge] = HalfEdge()
                if next_edge not in self.half_edges.keys():
                    self.half_edges[next_edge] = HalfEdge()
                if pair not in self.half_edges.keys():
                    self.half_edges[pair] = HalfEdge()

                self.half_edges[edge].vertex = self.vertices[edge[0]]
                self.half_edges[edge].next_edge = self.half_edges[next_edge]
                self.half_edges[next_edge].prev_edge = self.half_edges[edge]
                self.half_edges[edge].pair = self.half_edges[pair]

                self.vertices[edge[0]].edge = self.half_edges[edge]

            face_ob = HEFace(self.half_edges[edges[0]])
            for e in xrange(len(edges)):
                edge = edges[e]
                self.half_edges[edge].face = face_ob
            self.faces.append(face_ob)

    def __find_edges_from_vertex(self, vertex):
        edges = [vertex.edge]
        edge = vertex.edge
        while True:
            edge = edge.pair.prev_edge
            if edge == edges[0]:
                break
            edges.append(edge)
        return edges

    def __find_vertices_surrounding_vertex(self, vertex):
        edges = self.__find_edges_from_vertex(vertex)
        vertices = set()
        for edge in edges:
            vertices.add(edge.vertex)
            vertices.add(edge.pair.vertex)
        vertices.remove(vertex)
        return vertices

    def __find_face_edges(self, face):
        edges = [face.edge]
        edge = edges[0]
        while True:
            edge = edge.next_edge
            if edge == edges[0]:
                break
            edges.append(edge)
        return edges

    def __find_joining_edge(self, face1, face2):
        face1_edges = self.__find_face_edges(face1)
        face2_edges = self.__find_face_edges(face2)
        for f1 in face1_edges:
            for f2 in face2_edges:
                if f1.pair == f2:
                    return f1

    def vertex_surrounding(self, vertex_id):
        vertex = self.vertices[vertex_id]
        first_layer = self.__find_vertices_surrounding_vertex(vertex)
        second_layer = set()
        for v in first_layer:
            tmp = self.__find_vertices_surrounding_vertex(v)
            second_layer = second_layer.union(tmp)
        second_layer = second_layer.difference(first_layer)
        second_layer.remove(vertex)
        return first_layer, second_layer

    def elements_with_vertex(self, vertex_id):
        vertex = self.vertices[vertex_id]
        edges = self.__find_edges_from_vertex(vertex)
        faces = []
        for edge in edges:
            faces.append(edge.face)
        return edges, faces

    def face_surrounding(self, face_id):
        face = self.faces[face_id]
        face_edges = self.__find_face_edges(face)
        faces = []
        for edge in face_edges:
            faces.append(edge.pair.face)
        return faces

    def switch_triangles(self, face_id1, face_id2):
        face1 = self.faces[face_id1]
        face2 = self.faces[face_id2]
        join_edge = self.__find_joining_edge(face1, face2)

        # TODO add arguments checking
        pair_edge = join_edge.pair

        # change faces
        join_edge.face.edge = join_edge.next_edge
        pair_edge.face.edge = pair_edge.next_edge

        # change half edge
        new_edge1 = HalfEdge()
        new_edge1.face = face1
        new_edge1.vertex = face1.edge.next_edge.vertex
        face1.edge.next_edge.vertex.edge = new_edge1
        new_edge1.prev_edge = face1.edge
        new_edge1.next_edge = face1.edge.prev_edge

        new_edge2 = HalfEdge()
        new_edge1.pair = new_edge2
        new_edge2.pair = new_edge1

        new_edge2.vertex = face2.edge.next_edge.vertex
        face2.edge.next_edge.vertex.edge = new_edge2.vertex
        new_edge2.prev_edge = face2.edge
        new_edge2.next_edge = face2.edge.prev_edge

    def mesh_boundary(self):
        for vertex in self.vertices:
            edges_num = len(self.__find_edges_from_vertex(vertex))
            if edges_num == 1:
                return False
        return True


if __name__ == '__main__':
    pass
