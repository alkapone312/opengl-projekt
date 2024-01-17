import glm
from OpenGL.GL import *
import pygame as pg

class Camera:
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        self.position = position
        self.orientation = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.cameraMatrix = glm.mat4(1.0)

        self.speed = 0.03
        self.sensitivity = 50

        self.lastX = 0
        self.lastY = 0

    def updateMatrix(self, fov, near, far):
        view = glm.mat4()
        proj = glm.mat4()

        view = glm.lookAt(self.position, self.position + self.orientation, self.up)
        proj = glm.perspective(glm.radians(fov), self.width/self.height, near, far)

        self.cameraMatrix = proj * view

    def matrix(self, shader, uniform):
        projLoc = glGetUniformLocation(shader.ID, uniform)
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(self.cameraMatrix))


    def inputs(self, event):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.speed * self.orientation
        if keys[pg.K_a]:
            self.position += self.speed * -glm.normalize(glm.cross(self.orientation, self.up))
        if keys[pg.K_s]:
            self.position -= self.speed * self.orientation
        if keys[pg.K_d]:
            self.position += self.speed * glm.normalize(glm.cross(self.orientation, self.up))
        if keys[pg.K_SPACE]:
            self.position += self.speed * self.up
        if keys[pg.K_LCTRL]:
            self.position += self.speed * -self.up

        if pg.mouse.get_pressed()[0] == True:
            mouseX, mouseY = pg.mouse.get_pos()
            deltaX = mouseX - self.width/2
            deltaY = mouseY - self.height/2
            pg.mouse.set_visible(False)
            pg.event.set_grab(True)
            pg.mouse.set_pos(self.width/2, self.height/2)
            rotX = self.sensitivity * (deltaY) / self.height
            rotY = self.sensitivity * (deltaX) / self.width

            self.orientation = glm.rotate(self.orientation, glm.radians(-rotX), glm.normalize(glm.cross(self.orientation, self.up)))
            self.orientation = glm.rotate(self.orientation, glm.radians(-rotY), self.up)
        else:
            pg.mouse.set_visible(True)
            pg.event.set_grab(False)
    def setPosition(self, position):
        self.position = position

    def setOrientation(self, orientation):
        self.orientation = orientation

    def getOrientation(self):
        return self.orientation
    
    def getPosition(self):
        return self.position