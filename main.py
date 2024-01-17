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
from Model.Mesh import Mesh
from Model.Plane import Plane
from Model.Tetrahedron import Tetrahedron
from Model.VerticesTransformer import VerticesTransformer
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
    metalTextures = [
        Texture("textures/metal/metal.jpg", "diffuse", 0),
        Texture("textures/metal/specular.jpg", "specular", 1),
    ]
    woodTextures = [
        Texture("textures/wood/wood.jpg", "diffuse", 0),
        Texture("textures/wood/specular.jpg", "specular", 1),
    ]
    rockTextures = [
        Texture("textures/rock/rock.jpg", "diffuse", 0),
    ]
    basicShader = Shader()
    lightShader = Shader("shaders/light.vert", "shaders/light.frag")

    birdVertices = VerticesTransformer(ObjLoader().load('models/bird.obj').vertices).scale(0.005, 0.005, 0.005)
    birdVertices = VerticesTransformer(birdVertices).translate(-0.1, 0.31, -4.5)
    mausoleumVertices = VerticesTransformer(ObjLoader().load('models/mausoleum.obj').vertices).scale(0.01, 0.01, 0.01)
    mausoleumVertices = VerticesTransformer(mausoleumVertices).translate(0, 0.8, -4)
    lampVertices = VerticesTransformer(ObjLoader().load('models/lamp.obj').vertices).scale(0.009,0.009,0.009)
    lampVertices2 = VerticesTransformer(lampVertices).rotate(0, 180, 0)
    lamps = [
        VerticesTransformer(lampVertices).translate(-0.5, 0, -2),
        VerticesTransformer(lampVertices2).translate(0.5, 0, -2),
        VerticesTransformer(lampVertices).translate(-0.5, 0, -1),
        VerticesTransformer(lampVertices2).translate(0.5, 0, -1),
        VerticesTransformer(lampVertices).translate(-0.5, 0, 0),
        VerticesTransformer(lampVertices2).translate(0.5, 0, 0),
    ]
    commodeVertices = VerticesTransformer(ObjLoader().load('models/commode.obj').vertices).scale(0.01, 0.01, 0.01)
    commodeVertices = VerticesTransformer(commodeVertices).rotate(0, -90, 0)
    commodeVertices = VerticesTransformer(commodeVertices).translate(0, 0.15, -4.5)
    pyramidModel = SierpinskiPyramid(basicShader, rockTextures)
    pyramidModel.startMesh = Mesh(VerticesTransformer(pyramidModel.startMesh.vertices).scale(0.1, 0.1, 0.1))
    pyramidModel.startMesh = Mesh(VerticesTransformer(pyramidModel.startMesh.vertices).translate(0.1, 0.03, -4.5))
    pyramidModel.mesh = pyramidModel.startMesh
    bird = Model(Mesh(birdVertices), basicShader, birdTextures)
    mausoleum = Model(Mesh(mausoleumVertices), basicShader, plankTextures)
    commode = Model(Mesh(commodeVertices), basicShader, woodTextures)
    for i in range(len(lamps)):
        lamps[i] = Model(Mesh(lamps[i]), basicShader, metalTextures)
    floorModel = Plane(basicShader, grassTexture, 100, 100)
    lightModel = Cube(lightShader, [])

    models = [
        floorModel,
        lightModel,
        mausoleum,
        commode,
        pyramidModel,
        bird
    ]
    models.extend(lamps)

    lightPos = glm.vec3(5, 5, 5)
    skybox = Skybox('stars')
    renderer = Renderer()
    camera = Camera(display[0], display[1], glm.vec3(0, 0.5, 2))
    glViewport(0, 0, display[0], display[1]);
    glEnable(GL_DEPTH_TEST)
    pyramidModel.translate(0, 0.15, 0)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            camera.inputs(event)
        glClearColor(0.07, 0.13, 0.17, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.updateMatrix(45, 0.1, 100)
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
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            pyramidModel.nextLevel()
            pg.time.wait(200)
        if keys[pg.K_q]:
            pyramidModel.previousLevel()
            pg.time.wait(200)

if __name__ == "__main__":
    main()
