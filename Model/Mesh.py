import numpy
from OpenGL.GL import *
from ctypes import *

from Model.VertexArray import VertexArray
from Model.VertexBuffer import VertexBuffer
from Model.ElementBuffer import ElementBuffer

class Mesh:
    def __init__(self, vertices = numpy.array([], dtype="float32"), indices = numpy.array([], dtype="uint32")):
        self.vertices = vertices
        self.indices = indices

        self.vertexArray = VertexArray()
        self.vertexArray.bind()

        vertexBuffer = VertexBuffer(vertices)
        elementBuffer = ElementBuffer(indices)

        float_size = 4
        self.vertexArray.linkAttrib(vertexBuffer, 0, 3, GL_FLOAT, 8 * float_size, ctypes.c_void_p(0))
        self.vertexArray.linkAttrib(vertexBuffer, 1, 3, GL_FLOAT, 8 * float_size, ctypes.c_void_p(3 * float_size))
        self.vertexArray.linkAttrib(vertexBuffer, 2, 2, GL_FLOAT, 8 * float_size, ctypes.c_void_p(6 * float_size))
        self.vertexArray.unbind()
        vertexBuffer.unbind()
        elementBuffer.unbind()

    def getVertices(self):
        return self.vertices
    
    def getIndices(self):
        return self.indices
