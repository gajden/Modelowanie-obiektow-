from processing.loader import DataLoader


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


class HalfEdgeStructure(object):
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
        print 'HE', self.half_edges
        print 'face', self.faces
        print 'ver', self.vertices

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

    def get_surrounding_vertices_for_vertex(self, vertex_id):
        vertex = self.vertices[vertex_id]
        first_layer = self.__find_vertices_surrounding_vertex(vertex)
        second_layer = set()
        for v in first_layer:
            tmp = self.__find_vertices_surrounding_vertex(v)
            second_layer = second_layer.union(tmp)
        second_layer = second_layer.difference(first_layer)
        second_layer.remove(vertex)
        return first_layer, second_layer

    def get_elements_containing_vertex(self, vertex_id):
        vertex = self.vertices[vertex_id]
        edges = self.__find_edges_from_vertex(vertex)
        faces = []
        for edge in edges:
            print edge.face
            faces.append(edge.face)
        return edges, faces

    def get_surrounding_elements_for_element(self, element_id):
        pass

    def change_edges(self, face1, face2):
        pass

    def grid_has_edge(self):
        pass


if __name__ == '__main__':
    path = '../files/ex.ply'
    loader = DataLoader()
    p = loader.load_file(path)
    # print p
    he = HalfEdgeStructure(p['vertex'], p['edge'], p['face'])
    first, second = he.get_surrounding_vertices_for_vertex(2)
    edges, faces = he.get_elements_containing_vertex(0)

    print edges
    print faces

    print 'First'
    for v in first:
        print v
    print ''
    print 'Second'
    for v in second:
        print v
