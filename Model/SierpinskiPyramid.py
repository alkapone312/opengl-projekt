import numpy
from Model.Tetrahedron import Tetrahedron
from Model.Mesh import Mesh
from Model.Model import Model
from Model.VerticesTransformer import VerticesTransformer

class SierpinskiPyramid(Model):
    def __init__(self, shader, textures):
        self.level = 0
        self.shader = shader
        self.textures = textures
        self.startMesh = Tetrahedron(self.shader, self.textures).mesh
        super().__init__(
            self.startMesh,
            shader,
            textures
        )
        self.update()
        
    def nextLevel(self):
        self.level += 1
        self.update()


    def previousLevel(self):
        if self.level > 0:
            self.level -= 1
            self.update()
        
    def update(self):
        buff = [self.startMesh]
        for i in range(self.level):
            a = []
            for mesh in buff:
                newMeshes = [
                    Mesh(VerticesTransformer(mesh.getVertices(), 8).translate(
                        mesh.getVertices()[8 * 0], 
                        mesh.getVertices()[8 * 0 + 1], 
                        mesh.getVertices()[8 * 0 + 2]
                    )),
                    Mesh(VerticesTransformer(mesh.getVertices(), 8).translate(
                        mesh.getVertices()[8 * 1], 
                        mesh.getVertices()[8 * 1 + 1], 
                        mesh.getVertices()[8 * 1 + 2]
                    )),
                    Mesh(VerticesTransformer(mesh.getVertices(), 8).translate(
                        mesh.getVertices()[8 * 2], 
                        mesh.getVertices()[8 * 2 + 1], 
                        mesh.getVertices()[8 * 2 + 2]
                    )),
                    Mesh(VerticesTransformer(mesh.getVertices(), 8).translate(
                        mesh.getVertices()[8 * 4], 
                        mesh.getVertices()[8 * 4 + 1], 
                        mesh.getVertices()[8 * 4 + 2]
                    ))
                ]
                for newMesh in newMeshes:
                    newMesh.vertices = VerticesTransformer(newMesh.vertices, 8).scale(0.5, 0.5, 0.5)
                    a.append(newMesh)
            buff = a 
        vertices = []
        for mesh in buff:
            vertices.extend(mesh.vertices)
        self.mesh = Mesh(numpy.array(vertices, dtype='float32'))