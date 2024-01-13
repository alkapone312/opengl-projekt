import math
import numpy
import ctypes

import pygame as pg
from pygame.locals import *

from stb import image

from OpenGL.GL import *
from OpenGL.GLU import *
import glm

from Shader import Shader
from Texture import Texture
from Camera import Camera
from Light import Light
from Renderer import Renderer
from Skybox import Skybox
from Model.Cube import Cube
from Model.Model import Model
from Model.Plane import Plane
from Model.Tetrahedron import Tetrahedron
from Loader.ObjLoader import ObjLoader

def main():
    pg.init()
    display = (1024, 1024)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    pg.display.set_caption("Piramida sierpinskiego - OpenGL")

    textures = [
        Texture("textures/planks.png", "diffuse", 0),
        Texture("textures/planksSpec.png", "specular", 1)
    ]
    basicShader = Shader("shaders/basic.vert", "shaders/basic.frag")
    lightShader = Shader("shaders/light.vert", "shaders/light.frag")

    torus = Model(ObjLoader().load('models/torus.obj'), basicShader, textures)

    floorModel = Plane(basicShader, textures)
    lightModel = Cube(lightShader,[])
    tetrahedronModel = Tetrahedron(basicShader, textures)
    cubeModel = Cube(basicShader, textures)

    models = [
        #floorModel,
        lightModel,
        tetrahedronModel,
        torus
    ]

    lightPos = glm.vec3(0.8, 0.8, 0.8)
    skybox = Skybox('sky')
    renderer = Renderer()
    camera = Camera(display[0], display[1], glm.vec3(0, 0.5, 2))
    glViewport(0, 0, display[0], display[1]);
    glEnable(GL_DEPTH_TEST)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            camera.inputs(event)
        glClearColor(0.07, 0.13, 0.17, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.updateMatrix(45, 0.1, 100)
        torus.rotateY(1)
        tetrahedronModel.rotateY(-1)
        skybox.draw(camera)
        lightPos = glm.rotate(0.02, glm.vec3(0, 1, 0)) * lightPos
        lightModel.translate(lightPos.x, lightPos.y, lightPos.z)
        lightModel.scale(0.1, 0.1, 0.1)
        for model in models:
            renderer.render(
                model,
                Light(
                    glm.vec4(1.0, 1.0, 1.0, 1.0),
                    glm.vec3(lightPos.x, lightPos.y, lightPos.z)
                ),
                camera
            )
        lightModel.scale(10, 10, 10)
        lightModel.translate(-lightPos.x, -lightPos.y, -lightPos.z)
        pg.display.flip()
        pg.time.wait(int(1000/30))

if __name__ == "__main__":
    main()
