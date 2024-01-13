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
        self.translateMatrix = glm.mat4(1)
        self.scaleMatrix = glm.mat4(1)

    def translate(self, x, y, z):
        self.model = glm.translate(self.model, glm.vec3(x, y, z))

    def rotateX(self, angle):
        self.model = glm.rotate(self.model, glm.radians(angle / 2), glm.vec3(1, 0, 0))

    def rotateY(self, angle):
        self.model = glm.rotate(self.model, glm.radians(angle / 2), glm.vec3(0, 1, 0))

    def rotateZ(self, angle):
        self.model = glm.rotate(self.model, glm.radians(angle / 2), glm.vec3(0, 0, 1))

    def scale(self, x, y, z):
        self.model = glm.scale(self.model, glm.vec3(x, y, z))

    def getModelMatrix(self):
        return self.model