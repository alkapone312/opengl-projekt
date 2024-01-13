from OpenGL.GL import *
from Model.VertexBuffer import VertexBuffer

class VertexArray:
    def __init__(self):
        self.ID = vertexArray = glGenVertexArrays(1)

    def linkAttrib(
            self, 
            vertexBuffer: VertexBuffer, 
            layout: int, 
            numberOfComponents: int, 
            type, 
            stride, 
            offset
        ):
        vertexBuffer.bind()
        glVertexAttribPointer(layout, numberOfComponents, type, GL_FALSE, stride, offset)
        glEnableVertexAttribArray(layout)
        vertexBuffer.unbind()

    def bind(self):
        glBindVertexArray(self.ID)

    def unbind(self):
        glBindVertexArray(0)

    def delete(self):
        glDeleteVertexArrays(1, self.ID)