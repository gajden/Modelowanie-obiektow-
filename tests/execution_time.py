import time

import sys

from processing.loader import DataLoader
from structures.face_vertex import FaceVertexStructure
from structures.half_edge import HalfEdgeStructure


def measure_time(fun, *args):
    start = time.time()
    res = fun(*args)
    end = time.time()
    return end - start, res

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s file_name' % sys.argv[0]
        sys.exit()
    filename = sys.argv[1]

    loader = DataLoader()
    data = loader.load_file(filename)
    he = HalfEdgeStructure(data['vertex'], data['edge'], data['face'])
    fv = FaceVertexStructure(filename)

    print 'Execution time of vertex_surrounding:'
    print 'HE: %fs' % measure_time(he.vertex_surrounding, 0)[0]
    print 'FV: %fs\n' % measure_time(fv.vertex_surrounding, 0)[0]

    print 'Execution time of elements_with_vertex:'
    print 'HE: %fs' % measure_time(he.elements_with_vertex, 0)[0]
    print 'FV: %fs\n' % measure_time(fv.elements_with_vertex, 0)[0]

    print 'Execution time of face_surrounding:'
    print 'HE: %fs' % measure_time(he.face_surrounding, 1)[0]
    print 'FV: %fs\n' % measure_time(fv.face_surrounding, 1)[0]

    print 'Execution time of switch_triangles:'
    face_neig = he.face_surrounding(1)[0]
    print 'HE: %fs' % measure_time(he.switch_triangles, 1, face_neig)[0]
    face_neig = fv.face_surrounding(1)[0]
    print 'FV: %fs\n' % measure_time(fv.switch_triangles, 1, face_neig)[0]

    print 'Execution time of mesh_boundary:'
    print 'HE: %f' % measure_time(he.mesh_boundary)[0]
    print 'FV: %f\n' % measure_time(fv.mesh_boundary)[0]
