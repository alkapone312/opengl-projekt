import numpy
import glm
from Model.Model import Model
from Model.Mesh import Mesh
from Model.VerticesTransformer import VerticesTransformer

class Tetrahedron(Model):
    def __init__(self, shader, textures):
        normals = [
            -glm.cross(glm.vec3(-0.5, -0.5, -0.5), glm.vec3(-0.5, 0.5, 0.5)), # 0, 1
            -glm.cross(glm.vec3(-0.5, -0.5, -0.5), glm.vec3( 0.5, 0.5,-0.5)), # 3, 4
            -glm.cross(glm.vec3( 0.5,  0.5, -0.5), glm.vec3( 0.5,-0.5, 0.5)), # 6, 7
             glm.cross(glm.vec3(-0.5, -0.5, -0.5), glm.vec3( 0.5, 0.5,-0.5))  # 9, 10
        ]
        vertices = numpy.array([
            -0.5, -0.5, -0.5,   normals[0].x, normals[0].y, normals[0].z,  0.0, 0.0,
            -0.5,  0.5,  0.5,   normals[0].x, normals[0].y, normals[0].z,  1.0, 0.0,
             0.5, -0.5,  0.5,   normals[0].x, normals[0].y, normals[0].z,  1.0, 1.0, 

            -0.5, -0.5, -0.5,   normals[1].x, normals[1].y, normals[1].z,  0.0, 0.0,
             0.5,  0.5, -0.5,   normals[1].x, normals[1].y, normals[1].z,  1.0, 0.0,
            -0.5,  0.5,  0.5,   normals[1].x, normals[1].y, normals[1].z,  1.0, 1.0, 

             0.5,  0.5, -0.5,   normals[2].x, normals[2].y, normals[2].z,  0.0, 0.0,
             0.5, -0.5,  0.5,   normals[2].x, normals[2].y, normals[2].z,  1.0, 0.0,
            -0.5,  0.5,  0.5,   normals[2].x, normals[2].y, normals[2].z,  1.0, 1.0, 

            -0.5, -0.5, -0.5,   normals[3].x, normals[3].y, normals[3].z,  0.0, 0.0,
             0.5,  0.5, -0.5,   normals[3].x, normals[3].y, normals[3].z,  1.0, 0.0,
             0.5, -0.5,  0.5,   normals[3].x, normals[3].y, normals[3].z,  1.0, 1.0, 
        ], dtype="float32")

        indices = numpy.array([
            0, 1, 2,
            3, 4, 5,
            6, 7, 8,
            9, 10, 11
        ], dtype='uint32')

        vertices = VerticesTransformer(vertices, 8).rotate(0, 45, 0)
        vertices = VerticesTransformer(vertices, 8).rotate(-glm.degrees(glm.atan(1/(2**0.5/2))), 0, 0)

        super().__init__(Mesh(vertices, indices), shader, textures)
