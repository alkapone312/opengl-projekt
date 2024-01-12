import pygame as pg
from OpenGL.GL import *
from Shader import Shader

class Texture:
    def __init__(self, texPath, texType, slot):
        self.texType = texType
        textureImg = pg.image.load(texPath)
        textureImg = pg.transform.flip(textureImg, False, True)
        width, height = textureImg.get_size()
        numberOfColorChannels = textureImg.get_bytesize()
        bytes = textureImg.get_buffer().raw
        self.ID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + slot)
        self.unit = slot
        glBindTexture(GL_TEXTURE_2D, self.ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        if texType == 'normal':
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes)
        elif numberOfColorChannels == 4:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes)
        elif numberOfColorChannels == 3:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, bytes)
        elif numberOfColorChannels == 1:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RED, GL_UNSIGNED_BYTE, bytes)
        else:
            print("Cannot determine texture type.")
            exit()
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