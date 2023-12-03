import math
import numpy

import pygame as pg
from pygame.locals import *

from stb import image

from OpenGL.GL import *
from OpenGL.GLU import *

from Shader import Shader
from Texture import Texture
from VertexArray import VertexArray
from VertexBuffer import VertexBuffer
from ElementBuffer import ElementBuffer

def main():
    pg.init()
    display = (800, 800)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    pg.display.set_caption("Piramida sierpińskiego - OpenGL")

    vertices = numpy.array([
        -0.5, -0.5,  0.0,    1.0, 0.0, 0.0,  0.0, 0.0,
        -0.5,  0.5,  0.0,    0.0, 1.0, 0.0,  0.0, 1.0,
         0.5,  0.5,  0.0,    0.0, 0.0, 1.0,  1.0, 1.0,
         0.5, -0.5,  0.0,    1.0, 1.0, 1.0,  1.0, 0.0
    ], dtype='float32')

    indices = numpy.array([
        0, 2, 1,
        0, 3, 2
    ], dtype='uint32')

    shader = Shader('shaders/basic.vert', 'shaders/basic.frag')

    vertexArray = VertexArray()
    vertexArray.bind()

    vertexBuffer = VertexBuffer(vertices)
    elementBuffer = ElementBuffer(indices)

    vertexArray.linkAttrib(vertexBuffer, 0, 3, GL_FLOAT, 8 * 4, ctypes.c_void_p(0))
    vertexArray.linkAttrib(vertexBuffer, 1, 3, GL_FLOAT, 8 * 4, ctypes.c_void_p(3 * 4))
    vertexArray.linkAttrib(vertexBuffer, 2, 2, GL_FLOAT, 8 * 4, ctypes.c_void_p(6 * 4))
    vertexArray.unbind()
    vertexBuffer.unbind()
    elementBuffer.unbind()

    texture = Texture("textures/earth.png", GL_TEXTURE_2D, GL_TEXTURE0, GL_RGBA, GL_UNSIGNED_BYTE)
    texture.texUni(shader, "tex0", 0)
    texture.unbind()
    

    glViewport(0, 0, display[0], display[1]);
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClearColor(0.07, 0.13, 0.17, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        shader.activate()
        texture.bind()
        vertexArray.bind()
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        pg.display.flip()
        pg.time.wait(10)


    vertexArray.delete()
    vertexBuffer.delete()
    elementBuffer.delete()
    texture.delete()
    shader.delete()

if __name__ == "__main__":
    main()