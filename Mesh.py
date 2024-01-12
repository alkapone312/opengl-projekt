import numpy
from OpenGL.GL import *
from ctypes import *

from VertexArray import VertexArray
from VertexBuffer import VertexBuffer
from ElementBuffer import ElementBuffer

class Mesh:
    def __init__(self, vertices = numpy.array([], dtype="float32"), indices = numpy.array([], dtype="uint32"), textures = []):
        self.vertices = vertices
        self.indices = indices
        self.textures = textures

        self.vertexArray = VertexArray()
        self.vertexArray.bind()

        vertexBuffer = VertexBuffer(vertices)
        elementBuffer = ElementBuffer(indices)

        float_size = 4
        self.vertexArray.linkAttrib(vertexBuffer, 0, 3, GL_FLOAT, 11 * float_size, ctypes.c_void_p(0))
        self.vertexArray.linkAttrib(vertexBuffer, 1, 3, GL_FLOAT, 11 * float_size, ctypes.c_void_p(3 * float_size))
        self.vertexArray.linkAttrib(vertexBuffer, 2, 3, GL_FLOAT, 11 * float_size, ctypes.c_void_p(6 * float_size))
        self.vertexArray.linkAttrib(vertexBuffer, 3, 2, GL_FLOAT, 11 * float_size, ctypes.c_void_p(9 * float_size))
        self.vertexArray.unbind()
        vertexBuffer.unbind()
        elementBuffer.unbind()

    def draw(self, shader, camera):
        shader.activate()
        self.vertexArray.bind()
        numDiffuse = 0
        numSpecular = 0
        numNormal = 0
        for i in range(0, len(self.textures)):
            num = ""
            type = self.textures[i].texType
            if type == "diffuse":
                num = numDiffuse
                numDiffuse += 1
            elif type == "specular":
                num = numSpecular
                numSpecular += 1
            elif type == "normal":
                num = numNormal
                numNormal += 1
            self.textures[i].texUni(shader, cast(type + str(num), c_char_p), i)
            self.textures[i].bind()
        glUniform3f(
            glGetUniformLocation(shader.ID, "camPos"), 
            camera.position.x, 
            camera.position.y, 
            camera.position.z
        )
        camera.matrix(shader, "camMatrix")

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)