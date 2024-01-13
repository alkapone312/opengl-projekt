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
from Model.Mesh import Mesh
from Light import Light
from Renderer import Renderer
from Model.Model import Model

def main():
    pg.init()
    display = (800, 800)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    pg.display.set_caption("Piramida sierpinskiego - OpenGL")

    vertices = numpy.array([
        # Position        # Normals        # Color          # Texture
        -1.0, 0.0, 1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   0.0, 0.0,
        -1.0, 0.0,-1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   0.0, 2.0,
         1.0, 0.0,-1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   2.0, 2.0,
         1.0, 0.0, 1.0,   0.0, 1.0, 0.0,   0.0, 0.0, 0.0,   0.0, 2.0
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
        Texture("textures/planks.png", "diffuse", 0),
        Texture("textures/planksSpec.png", "specular", 1)
    ]
    basicShader = Shader("shaders/basic.vert", "shaders/basic.frag")
    lightShader = Shader("shaders/light.vert", "shaders/light.frag")
    floorMesh = Mesh(vertices, indices)
    lightMesh = Mesh(lightVertices, lightIndices)

    floorModel = Model(
        floorMesh,
        basicShader,
        textures
    )

    lightModel = Model(
        lightMesh,
        lightShader,
        []
    )

    lightModel.translate(0.5, 0.5, 0.5)

    # floorModel.rotate(90, 1, 0, 0)

    renderer = Renderer()
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

        renderer.render(
            floorModel,
            Light(
                glm.vec4(1.0, 1.0, 1.0, 1.0),
                glm.vec3(0.5, 0.5, 0.5)
            ),
            camera
        )

        renderer.render(
            lightModel,
            Light(
                glm.vec4(1.0, 1.0, 1.0, 1.0),
                glm.vec3(0.5, 0.5, 0.5)
            ),
            camera
        )

        pg.display.flip()
        pg.time.wait(int(1000/30))

if __name__ == "__main__":
    main()