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
            self.__load_stl(path)

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
        return info

    def __load_stl(self, path):
        pass
