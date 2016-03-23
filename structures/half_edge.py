from processing.loader import DataLoader


class HalfEdge(object):
    def __init__(self, vertex=None, pair=None, face=None, next_edge=None):
        self.vertex = vertex
        self.pair = pair
        self.face = face
        self.next_edge = next_edge
        self.prev_edge = None
        self.number = None


class HEVertex(object):
    def __init__(self, number, coordinate, edge=None):
        self.number = number
        self.coordinate = coordinate
        self.edge = edge


class HEFace(object):
    def __init__(self, number, edge):
        self.number = number
        self.edge = edge


class HalfEdgeStructure(object):
    def __init__(self, vertex, edge, face):
        self.half_edges = {}
        self.vertices = []
        self.faces = []
        self.__build_structure(vertex, edge, face)

    def __build_structure(self, vertices, edges, faces, ccw=True):
        for idx, vertex in enumerate(vertices):
            self.vertices.append(HEVertex(idx, vertex))

        for idx, face in enumerate(faces):

            edges = [(face[i], face[(i+1) % len(face)]) for i in xrange(len(face))]
            print edges
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
                self.half_edges[edge].face = face
                self.half_edges[edge].vertex = edge[0]
                self.half_edges[edge].next_edge = self.half_edges[next_edge]
                self.half_edges[next_edge].prev_edge = self.half_edges[edge]
                self.half_edges[edge].pair = self.half_edges[pair]

                self.vertices[edge[0]].edge = self.half_edges[edge]
            self.faces.append(HEFace(idx, self.half_edges[edges[0]]))



if __name__ == '__main__':
    path = '../files/example.ply'
    loader = DataLoader()
    p = loader.load_file(path)
    print p
    he = HalfEdgeStructure(p['vertex'], p['edge'], p['face'])
