from structures.vertex_connection_array import *

if __name__ == '__main__':
    mesh = MeshArray()
    mesh.loadFromPly('files/example.ply')
    print mesh.edgeChange(0,1)
    print mesh.elements()
    print mesh.vertex()
    print mesh.check()
    print mesh.vertexFaces()
