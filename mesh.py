from processing.loader import DataLoader


class MeshStructure(object):
    def __init__(self):
        pass

    def loadFromPly(self):
        pass
    def loadFromStl(self):
        pass


class MeshArray(MeshStructure):
    def __init__(self):
        self.vertexes = []

    def loadFromPly(self):
        pass

    def loadFromStl(self):
        data = DataLoader().load_file('files/example.stl')
        for facet in data[1]:
            for vertex in facet['vertexes']:
                self.vertexes.append(vertex)
        self.vertexes = list(set(self.vertexes))
        self.connections = []
        for i in range(len(self.vertexes)):
            self.connections.append([])
        for facet in data[1]:
            a = self.vertexes.index(facet['vertexes'][0])
            b = self.vertexes.index(facet['vertexes'][1])
            c = self.vertexes.index(facet['vertexes'][2])
            self.connections[a].append(b)
            self.connections[a].append(c)
            self.connections[b].append(a)
            self.connections[b].append(c)
            self.connections[c].append(a)
            self.connections[c].append(b)
        for i in range(len(self.connections)):
            self.connections[i] = list(set(self.connections[i]))
        print self.vertexes
        print self.connections


class MeshHalfEdge(MeshStructure): # albo winged
    def __init__(self):
        pass
    def loadFromStl(self):
        pass
    def loadFromPly(self):
        pass