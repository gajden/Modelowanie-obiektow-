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

    def __load_stl(self, path):
        data = []
        with open(path, 'r') as file:
            for line in file:
                parsed = [x.replace('\n','') for x in line.split(' ') if x != '']
                if parsed[0] == 'solid':
                    name = parsed[1]
                elif parsed[0] == 'endsolid':
                    return data
                elif parsed[0] == 'facet':
                    facet = {'normal': (float(parsed[2]), float(parsed[3]), float(parsed[4])), 'vertexes': []}
                elif parsed[0] == 'vertex':
                    facet['vertexes'].append((float(parsed[1]), float(parsed[2]), float(parsed[3])))
                elif parsed[0] == 'endfacet':
                    data.append(facet)



if __name__ == '__main__':
    loader = DataLoader()
    ply_path = '../files/example.ply'
    loaded = loader.load_file(ply_path)
    print loaded
