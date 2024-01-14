import numpy
from Model.Mesh import Mesh
from Model.Model import Model
from Model.VerticesTransformer import VerticesTransformer

class Plane(Model):
    def __init__(self, shader, textures, x = 1, z = 1):
        vertices = numpy.array([
            # Position       # Normals        # Texture
            -1.0, 0.0, 1.0,  0.0, 1.0, 0.0,   0.0, 0.0,
            -1.0, 0.0,-1.0,  0.0, 1.0, 0.0,   0.0, 2 * z,
             1.0, 0.0,-1.0,  0.0, 1.0, 0.0,   2 * x, 2 * z,
             1.0, 0.0, 1.0,  0.0, 1.0, 0.0,   0.0, 2 * z
        ], dtype="float32")

        indices = numpy.array([
            0, 1, 2,
            0, 2, 3,
        ], dtype="uint32")

        vertices = VerticesTransformer(vertices, 8).scale(x, 1, z)

        super().__init__(Mesh(vertices, indices), shader, textures)