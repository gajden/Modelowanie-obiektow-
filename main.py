from structures.face_vertex import *

if __name__ == '__main__':
    mesh = FaceVertexStructure('files/example.stl')
    print mesh.face_neighbors()
    print mesh.vertex_neighbors()
    print mesh.vertex_faces()
    print mesh.triangle_edge_replace(0, 1)