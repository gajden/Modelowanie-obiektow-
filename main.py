from structures.vertex_connection_array import *

if __name__ == '__main__':
    mesh = MeshArray()
    mesh.loadFromStl('files/example.stl')
    mesh.elements()
    mesh.vertexFaces()
    mesh.edgeChange(10, 11)
    print mesh.vertex()