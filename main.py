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
from Model.SierpinskiPyramid import SierpinskiPyramid
from Loader.ObjLoader import ObjLoader

def main():
    pg.init()
    display = (1024, 1024)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    pg.display.set_caption("Piramida sierpinskiego - OpenGL")

    plankTextures = [
        Texture("textures/planks.png", "diffuse", 0),
        Texture("textures/planksSpec.png", "specular", 1)
    ]
    birdTextures = [
        Texture("textures/bird.jpg", "diffuse", 0),
    ]
    grassTexture = [
        Texture("textures/grass.png", "diffuse", 0),
    ]
    basicShader = Shader("shaders/basic.vert", "shaders/basic.frag")
    lightShader = Shader("shaders/light.vert", "shaders/light.frag")

    #bird = Model(ObjLoader().load('models/bird.obj'), basicShader, birdTextures)

    floorModel = Plane(basicShader, grassTexture)
    lightModel = Cube(lightShader,[])
    cubeModel = Cube(basicShader, plankTextures)
    pyramidModel = SierpinskiPyramid(basicShader, plankTextures)

    models = [
        floorModel,
        lightModel,
        #bird
        #pyramidModel
    ]

    lightPos = glm.vec3(0.8, 0.8, 0.8)
    skybox = Skybox('sky')
    renderer = Renderer()
    camera = Camera(display[0], display[1], glm.vec3(0, 0.5, 2))
    glViewport(0, 0, display[0], display[1]);
    glEnable(GL_DEPTH_TEST)
    # bird.scale(0.3,0.3,0.3)
    pyramidModel.translate(0, 0.15, 0)
    pressed = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            camera.inputs(event)
        glClearColor(0.07, 0.13, 0.17, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.updateMatrix(45, 0.1, 100)
        # skybox.draw(camera)
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
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            pyramidModel.nextLevel()
            pg.time.wait(200)
        if keys[pg.K_q]:
            pyramidModel.previousLevel()
            pg.time.wait(200)

if __name__ == "__main__":
    main()
