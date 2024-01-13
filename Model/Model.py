import numpy
import glm
from Model.Mesh import Mesh
from Texture import Texture
from OpenGL.GL import *


class Model:
    def __init__(self, mesh, shader, textures):
        self.mesh = mesh
        self.shader = shader
        self.textures = textures
        self.model = glm.mat4(1)

    def translate(self, x, y, z):
        self.model = glm.translate(self.model, glm.vec3(x, y, z))
    
    def rotate(self, angle, x, y, z):
        self.model = glm.rotate(self.model, glm.radians(angle/2), glm.vec3(x, y, z))
        print(glm.radians(angle))
        print(3.14 / 4)
        print(self.model)

    def scale(self, x, y, z):
        self.model = glm.scale(self.model, glm.vec3(x, y, z))