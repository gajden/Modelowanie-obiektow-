from mesh import *

if __name__ == '__main__':
    mesh = MeshArray()
    mesh.loadFromStl('files/example.stl')
    print mesh.elements()
    print mesh.vertexFaces()
    mesh.edgeChange(10, 11)