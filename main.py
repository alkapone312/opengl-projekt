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
from Mesh import Mesh

def main():
    pg.init()
    display = (800, 800)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    pg.display.set_caption("Piramida sierpinskiego - OpenGL")

    vertices = numpy.array([
        # Position        # Normals        # Color          # Texture
        -1.0, 0.0, 1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   0.0, 0.0,
        -1.0, 0.0,-1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   0.0, 1.0,
         1.0, 0.0,-1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   1.0, 1.0,
         1.0, 0.0, 1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   0.0, 1.0
    ], dtype="float32")

    indices = numpy.array([
        0, 1, 2,
        0, 2, 3,
    ], dtype="uint32")

    lightVertices = numpy.array([
        -0.1, -0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
        -0.1, -0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
         0.1, -0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
         0.1, -0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
        -0.1,  0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
        -0.1,  0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
         0.1,  0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
         0.1,  0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
    ], dtype="float32")

    lightIndices = numpy.array([
        0, 1, 2,
        0, 2, 3,
        0, 4, 7,
        0, 7, 3,
        3, 7, 6,
        3, 6, 2,
        2, 6, 5,
        2, 5, 1,
        1, 5, 4,
        1, 4, 0,
        4, 5, 6,
        4, 6, 7
    ], dtype="uint32")

    textures = [
        Texture("textures/planks.png", "diffuse", 0, GL_RGBA, GL_UNSIGNED_BYTE),
        Texture("textures/planksSpec.png", "specular", 1, GL_RED, GL_UNSIGNED_BYTE)
    ]
    shader = Shader("shaders/basic.vert", "shaders/basic.frag")
    lightShader = Shader("shaders/light.vert", "shaders/light.frag");
    floor = Mesh(vertices, indices, textures)
    light = Mesh(lightVertices, lightIndices, textures)

    lightColor = glm.vec4(1.0, 1.0, 1.0, 1.0)

    lightPos = glm.vec3(0.5, 0.5, 0.5)
    lightModel = glm.mat4(1.0)
    lightModel = glm.translate(lightModel, lightPos)

    pyramidPos = glm.vec3(0.0, 0.0, 0.0)
    pyramidModel = glm.mat4(1.0)
    pyramidModel = glm.translate(pyramidModel, pyramidPos)

    lightShader.activate()
    glUniformMatrix4fv(glGetUniformLocation(lightShader.ID, "model"), 1, GL_FALSE, glm.value_ptr(lightModel))
    glUniform4f(glGetUniformLocation(lightShader.ID, "lightColor"), lightColor.x, lightColor.y, lightColor.z, lightColor.w)
    shader.activate()
    glUniformMatrix4fv(glGetUniformLocation(shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(pyramidModel))
    glUniform4f(glGetUniformLocation(shader.ID, "lightColor"), lightColor.x, lightColor.y, lightColor.z, lightColor.w)
    glUniform3f(glGetUniformLocation(shader.ID, "lightPos"), lightPos.x, lightPos.y, lightPos.z)
    camera = Camera(display[0], display[1], glm.vec3(0, 0.5, 2))
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

        camera.updateMatrix(45, 0.1, 100)

        floor.draw(shader, camera)
        light.draw(lightShader, camera)

        pg.display.flip()
        pg.time.wait(int(1000/30))

if __name__ == "__main__":
    main()