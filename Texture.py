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
        glBindTexture(texType, self.ID)
        glTexParameteri(texType, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(texType, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(texType, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(texType, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(texType, 0, GL_RGBA, width, height, 0, format, pixelType, bytes)
        glGenerateMipmap(texType)
        
        glBindTexture(texType, 0)

    def texUni(self, shader: Shader, uniformName, unit):
        texUni = glGetUniformLocation(shader.ID, uniformName)
        shader.activate()
        glUniform1i(texUni, unit)

    def bind(self):
        glActiveTexture(GL_TEXTURE0 + self.unit)
        glBindTexture(self.texType, self.ID)

    def unbind(self):
        glBindTexture(self.texType, 0)

    def delete(self):
        glDeleteTextures(1, self.ID)