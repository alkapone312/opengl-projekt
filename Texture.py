import pygame as pg
from OpenGL.GL import *
from Shader import Shader

class Texture:
    def __init__(self, texPath, texType, slot, format, pixelType):
        self.texType = texType
        textureImg = pg.image.load(texPath)
        textureImg = pg.transform.flip(textureImg, False, True)
        width, height = textureImg.get_size()
        bytes = textureImg.get_buffer().raw
        self.ID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + slot)
        self.unit = slot
        glBindTexture(GL_TEXTURE_2D, self.ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, format, pixelType, bytes)
        glGenerateMipmap(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, 0)

    def texUni(self, shader: Shader, uniformName, unit):
        shader.activate()
        glUniform1i(glGetUniformLocation(shader.ID, uniformName), unit)

    def bind(self):
        glActiveTexture(GL_TEXTURE0 + self.unit)
        glBindTexture(GL_TEXTURE_2D, self.ID)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def delete(self):
        glDeleteTextures(1, self.ID)