from collections import OrderedDict
from processing.exceptions import FileNotSupportedException


class DataLoader(object):
    def __init__(self):
        self.supported = ['ply', 'stl']

    def load_file(self, path):
        extension = path.split('.')[-1]
        if extension not in self.supported:
            raise FileNotSupportedException(0, 'Extension: .%s not supported.' % extension)
        elif extension == 'ply':
            return self.__load_ply(path)
        elif extension == 'stl':
            return self.__load_stl(path)

    def __load_ply(self, path):
        with open(path, 'rb') as f:
            info = self.__parse_ply_header(path)
            data = {}
            line = f.readline()

            while line[0] != 'end_header':
                line = f.readline().strip().split(' ')
            for element in info['element'].keys():
                data[element] = []
                for i in xrange(info['element'][element]['number']):
                    line = f.readline().strip().split(' ')
                    if element == 'vertex':
                        point = (float(line[0]), float(line[1]), float(line[2]))
                        data[element].append(point)
                    elif element == 'face':
                        vertices_num = int(line[0])
                        face = []
                        for v in xrange(1, vertices_num + 1):
                            face.append(int(line[v]))
                        data[element].append(face)
                    elif element == 'edge':
                        edge = [int(line[0]), int(line[1])]
                        data[element].append(edge)
            return data

    def __parse_ply_header(self, path):
        with open(path, 'rb') as f:
            last_element = None
            info = {'comment': [],
                    'element': OrderedDict()}
            line = f.readline().split(' ')[0]
            while line[0] != 'end_header':
                if line[0] == 'comment':
                    # TODO handle comments if needed
                    pass
                elif line[0] == 'format':
                    info[line[0]] = [line[1], line[2]]
                elif line[0] == 'element':
                    last_element = line[1]
                    info['element'][last_element] = OrderedDict()
                    info['element'][last_element]['number'] = int(line[2])
                elif line[0] == 'property':
                    info['element'][last_element][line[2]] = line[1]
                line = f.readline().strip().split(' ')
            return info

    @staticmethod
    def __load_stl(path):
        vertex_dict = dict()
        vertex_counter = 0
        last_vertex = None
        data = {
            'edge': [],
            'vertex': [],
            'face': []
        }
        with open(path, 'r') as f:
            for line in f:
                parsed = [x.replace('\n', '') for x in line.split(' ') if x != '']
                if parsed[0] == 'facet':
                    current_vertexes = []
                    current_edges = []
                elif parsed[0] == 'vertex':
                    vertex = (float(parsed[1]), float(parsed[2]), float(parsed[3]))
                    if vertex not in vertex_dict:
                        vertex_dict[vertex] = vertex_counter
                        vertex_counter += 1
                    current_vertexes.append(vertex)
                    if last_vertex is not None:
                        current_edges.append((vertex_dict[last_vertex], vertex_dict[vertex]))
                    last_vertex = vertex
                elif parsed[0] == 'endfacet':
                    current_edges.append((current_edges[1][1], current_edges[0][0]))
                    for edge in current_edges:
                        data['edge'].append(edge)
                    data['face'].append(tuple([vertex_dict[v] for v in current_vertexes]))
                    current_edges = []
                    current_vertexes = []
                    last_vertex = None
                elif parsed[0] == 'endsolid':
                    data['vertex'] = []
                    for i in range(len(vertex_dict)):
                        data['vertex'].append(None)
                    for vertex, index in vertex_dict.iteritems():
                        data['vertex'][index] = vertex
                    return data

if __name__ == '__main__':
    loader = DataLoader()
    ply_path = '../files/example.ply'
    loaded = loader.load_file(ply_path)
    print loaded
