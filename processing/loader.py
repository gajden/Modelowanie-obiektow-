from collections import OrderedDict
from processing.exceptions import FileNotSupportedException
import numpy as np


class DataLoader(object):
    def __init__(self):
        self.supported = ['ply', 'stl']

    def load_file(self, path):
        extension = path.split('.')[-1]
        if extension not in self.supported:
            raise FileNotSupportedException(0, 'Extension: .%s not supported.' % extension)
        elif extension == 'ply':
            self.__load_ply(path)
        elif extension == 'stl':
            return self.__load_stl(path)

    def __load_ply(self, path):
        with open(path, 'rb') as f:
            info = self.__parse_ply_header(path)
            data = {}
            line = f.readline()
            vertex = np.zeros((info['element']['vertex']['num'], 3))

            while line != 'end header':
                line = f.readline()


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
                    info[last_element] = {'number': int(line[2])}
                elif line[0] == 'property':
                    info[last_element][line[2]] = line[1]
                line = f.readline().split(' ')
        return info

    def __load_stl(self, path):
        name = ''
        data = []
        with open(path, 'r') as file:
            for line in file:
                parsed = [x.replace('\n','') for x in line.split(' ') if x != '']
                if parsed[0] == 'solid':
                    name = parsed[1]
                elif parsed[0] == 'endsolid':
                    return (name, data)
                elif parsed[0] == 'facet':
                    facet = {'normal': (float(parsed[2]), float(parsed[3]), float(parsed[4])), 'vertexes': []}
                elif parsed[0] == 'vertex':
                    facet['vertexes'].append((float(parsed[1]), float(parsed[2]), float(parsed[3])))
                elif parsed[0] == 'endfacet':
                    data.append(facet)
