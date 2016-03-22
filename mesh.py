from processing.loader import DataLoader
from processing.exceptions import IncorrectElementsException

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

    # sasiedztwo wierzcholkow dla kazdego wierzcholka, 2 warstwy
    def vertex(self):
        result = []
        for i in range(len(self.vertexes)):
            result.append([])
        for element in self.connections:
            result[element[0]].append(element[1])
            result[element[0]].append(element[2])
            result[element[1]].append(element[0])
            result[element[1]].append(element[2])
            result[element[2]].append(element[0])
            result[element[2]].append(element[1])
        result2 = []
        for i in range(len(self.vertexes)):
            result2.append([])
        for element in self.connections:
            result2[element[0]] = result[element[0]] + result[element[1]] + result[element[2]]
            result2[element[1]] = result[element[0]] + result[element[1]] + result[element[2]]
            result2[element[2]] = result[element[0]] + result[element[1]] + result[element[2]]
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
                if len(set(elem + elem2)) in [4,5]:
                    result[elem].append(elem2)
        return result

    #zamiana krawedzi w dwoch przyleglych elementach
    def edgeChange(self, elem1index, elem2index):
        if (elem1index < 0 or elem1index >= len(self.connections) or elem2index < 0 or elem2index >= len(self.connections)):
            raise IncorrectElementsException
        if len(set(self.connections[elem1index] + self.connections[elem2index])) != 4:
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



class MeshHalfEdge(MeshStructure): # albo winged
    def __init__(self):
        pass
    def loadFromPly(self):
        pass
    def loadFromStl(self):
        pass