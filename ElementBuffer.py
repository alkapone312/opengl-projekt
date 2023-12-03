from OpenGL.GL import *

class ElementBuffer:
    def __init__(self, vertices):
        self.ID = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ID)

    def unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def delete(self):
        glDeleteBuffers(1, self.ID)