from processing.loader import DataLoader


class MeshStructure(object):
    def __init__(self):
        pass

    def loadFromPly(self):
        pass
    def loadFromStl(self):
        pass
    def vertexes(self):
        pass
    def vertexFaces(self):
        pass
    def elements(self):
        pass


class MeshArray(MeshStructure):
    def __init__(self):
        self.vertexes = []
        self.connections = []

    def loadFromPly(self):
        pass

    def loadFromStl(self, path):
        data = DataLoader().load_file(path)
        self.vertexes = []
        for facet in data[1]:
            for vertex in facet['vertexes']:
                self.vertexes.append(vertex)
        self.vertexes = list(set(self.vertexes))
        self.connections = []
        for facet in data[1]:
            a = self.vertexes.index(facet['vertexes'][0])
            b = self.vertexes.index(facet['vertexes'][1])
            c = self.vertexes.index(facet['vertexes'][2])
            self.connections.append((a,b,c))
        print self.vertexes
        print self.connections

    def vertexes(self):
        pass

    def vertexFaces(self):
        result = dict()
        for vertex in self.vertexes:
            result[vertex] = []
        for i in range(len(self.connections)):
            for vertex in self.connections[i]:
                result[self.vertexes[vertex]].append(i)
        return result

    def elements(self):
        result = dict()
        for elem in self.connections:
            result[elem] = []
            for elem2 in self.connections:
                if len(set(elem + elem2)) in [4,5,6]:
                    result[elem].append(elem2)
        return result


class MeshHalfEdge(MeshStructure): # albo winged
    def __init__(self):
        pass
    def loadFromPly(self):
        pass
    def loadFromStl(self):
        pass