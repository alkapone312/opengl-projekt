import numpy
from Model.Mesh import Mesh
from Model.Model import Model

class Plane(Model):
    def __init__(self, shader, textures):
        vertices = numpy.array([
            # Position       # Normals        # Texture
            -1.0, 0.0, 1.0,  0.0, 1.0, 0.0,   0.0, 0.0,
            -1.0, 0.0,-1.0,  0.0, 1.0, 0.0,   0.0, 1.0,
             1.0, 0.0,-1.0,  0.0, 1.0, 0.0,   1.0, 1.0,
             1.0, 0.0, 1.0,  0.0, 1.0, 0.0,   0.0, 1.0
        ], dtype="float32")

        indices = numpy.array([
            0, 1, 2,
            0, 2, 3,
        ], dtype="uint32")

        super().__init__(Mesh(vertices, indices), shader, textures)