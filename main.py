import math
import numpy

import pygame as pg
from pygame.locals import *

from stb import image

from OpenGL.GL import *
from OpenGL.GLU import *
import glm

from Shader import Shader
from Texture import Texture
from Camera import Camera
from VertexArray import VertexArray
from VertexBuffer import VertexBuffer
from ElementBuffer import ElementBuffer

def main():
    pg.init()
    display = (800, 800)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    pg.display.set_caption("Piramida sierpinskiego - OpenGL")

    vertices = numpy.array([
        -0.5, 0.0,  0.5,    0.83, 0.70, 0.44,  0.0, 0.0,
        -0.5, 0.0, -0.5,    0.83, 0.70, 0.44,  1.0, 0.0,
         0.5, 0.0, -0.5,    0.83, 0.70, 0.44,  0.0, 0.0,
         0.5, 0.0,  0.5,    0.83, 0.70, 0.44,  1.0, 0.0,
         0.0, 0.8,  0.0,    0.92, 0.86, 0.76,  0.5, 1.0
    ], dtype='float32')

    indices = numpy.array([
        0, 1, 2,
        0, 2, 3,
        0, 1, 4,
        1, 2, 4,
        2, 3, 4,
        3, 0, 4
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

    texture = Texture("textures/grass.png", GL_TEXTURE_2D, GL_TEXTURE0, GL_RGBA, GL_UNSIGNED_BYTE)
    texture.texUni(shader, "tex0", 0)
    texture.unbind()
    
    camera = Camera(display[0], display[1], glm.vec3(0, 0, 2))
    angle = 1
    glViewport(0, 0, display[0], display[1]);
    glEnable(GL_DEPTH_TEST)
    while True:
        angle += 0.1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            camera.inputs(event)

        glClearColor(0.07, 0.13, 0.17, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shader.activate()

        camera.matrix(45, 0.1, 100, shader, 'camMatrix')

        texture.bind()
        vertexArray.bind()
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        pg.display.flip()
        pg.time.wait(int(1000/30))


    vertexArray.delete()
    vertexBuffer.delete()
    elementBuffer.delete()
    texture.delete()
    shader.delete()

if __name__ == "__main__":
    main()