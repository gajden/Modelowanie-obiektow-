from processing.loader import DataLoader
from processing.exceptions import IncorrectElementsException

class MeshArray():
    def __init__(self):
        self.vertexes = []
        self.connections = []

    def loadFromPly(self, path):
        data = DataLoader().load_file(path)
        self.vertexes = []
        self.connections = []
        for vertex in data['vertex']:
            self.vertexes.append(vertex)
        for face in data['face']:
            self.connections.append(tuple(face))
        print data

    def loadFromStl(self, path):
        data = DataLoader().load_file(path)
        self.vertexes = []
        for facet in data:
            for vertex in facet['vertexes']:
                self.vertexes.append(vertex)
        self.vertexes = list(set(self.vertexes))
        self.connections = []
        for facet in data:
            a = self.vertexes.index(facet['vertexes'][0])
            b = self.vertexes.index(facet['vertexes'][1])
            c = self.vertexes.index(facet['vertexes'][2])
            self.connections.append((a,b,c))
        print self.vertexes
        print self.connections

    # sasiedztwo wierzcholkow dla kazdego wierzcholka, 2 warstwy
    def vertex(self):
        result = []
        for i in range(len(self.vertexes)):
            result.append([])
        for element in self.connections:
            for i in range(len(element)):
                result[element[i]].append(element[(i+1)%len(element)])
                result[element[i]].append(element[(i+len(element)-1)%len(element)])
        result2 = []
        for i in range(len(self.vertexes)):
            result2.append([])
        for element in self.connections:
            for i in range(len(element)):
                result2[element[i]] = []
                for j in range(len(element)):
                    result2[element[i]] += result[element[j]]
        for i in range(len(result2)):
            result2[i] = set(result2[i])
        return result2

    # elementy zawierajace wierzcholek dla kazdego wierzcholka
    def vertexFaces(self):
        result = dict()
        for vertex in self.vertexes:
            result[vertex] = []
        for i in range(len(self.connections)):
            for vertex in self.connections[i]:
                result[self.vertexes[vertex]].append(i)
        return result

    #sasiedztwo elementow, 2 warstwy
    def elements(self):
        result = dict()
        for elem in self.connections:
            result[elem] = []
            for elem2 in self.connections:
                if len(set(elem + elem2)) < len(set(elem)) + len(set(elem2)):
                    result[elem].append(elem2)
        result2 = dict()
        for elem in self.connections:
            result2[elem] = []
            for elems in result[elem]:
                result2[elem] += result[elems]
        return result2

    #zamiana krawedzi w dwoch przyleglych elementach
    def edgeChange(self, elem1index, elem2index):
        if (elem1index < 0 or elem1index >= len(self.connections) or elem2index < 0 or elem2index >= len(self.connections)):
            raise IncorrectElementsException
        if len(set(self.connections[elem1index] + self.connections[elem2index])) > len(set(self.connections[elem1index])) + len(set(self.connections[elem2index])):
            raise IncorrectElementsException
        if len(self.connections[elem1index]) != 3 or len(self.connections[elem2index]) != 3:
            raise IncorrectElementsException
        set1 = set(self.connections[elem1index])
        set2 = set(self.connections[elem2index])
        intersection = set1 & set2
        other = list((set1 | set2) - intersection)
        intersection = list(intersection)
        self.connections[elem1index] = (other[0], other[1], intersection[0])
        self.connections[elem2index] = (other[0], other[1], intersection[1])

    #czy siatka posiada brzeg
    def check(self):
        vertexCounter = []
        for i in range(len(self.vertexes)):
            vertexCounter.append(0)
        for element in self.connections:
            for vertexIndex in element:
                vertexCounter[vertexIndex] += 1
        for v in vertexCounter:
            if v == 0:
                return False
        return True