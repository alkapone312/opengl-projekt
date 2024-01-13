import numpy
import glm
import pygame
from OpenGL.GL import *
from Shader import Shader

class Skybox:
    def __init__(self, skybox):
        self.skybox = skybox
        vertices = numpy.array([
            #   Coordinates
            -1.0, -1.0,  1.0,#        7--------6
            1.0, -1.0,  1.0, #       /|       /|
            1.0, -1.0, -1.0, #      4--------5 |
            -1.0, -1.0, -1.0,#      | |      | |
            -1.0,  1.0,  1.0,#      | 3------|-2
            1.0,  1.0,  1.0, #      |/       |/
            1.0,  1.0, -1.0, #      0--------1
            -1.0,  1.0, -1.0
        ], dtype='float32')

        indices = numpy.array([
            # Right
            1, 2, 6,
            6, 5, 1,
            # Left
            0, 4, 7,
            7, 3, 0,
            # Top
            4, 5, 6,
            6, 7, 4,
            # Bottom
            0, 3, 2,
            2, 1, 0,
            # Back
            0, 1, 5,
            5, 4, 0,
            # Front
            3, 7, 6,
            6, 2, 3
        ], dtype='uint32')

        # Generates Shader objects
        self.skyboxShader = Shader("shaders/skybox.vert", "shaders/skybox.frag")

        self.skyboxShader.activate()
        glUniform1i(glGetUniformLocation(self.skyboxShader.ID, "skybox"), 0)

        # Create VAO, VBO, and EBO for the skybox
        self.skyboxVAO = glGenVertexArrays(1)
        skyboxVBO = glGenBuffers(1)
        skyboxEBO = glGenBuffers(1)
        glBindVertexArray(self.skyboxVAO)
        glBindBuffer(GL_ARRAY_BUFFER, skyboxVBO)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, skyboxEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


        # All the faces of the cubemap (make sure they are in this exact order)
        folder = self.skybox
        facesCubemap = [
            'skyboxes/'+folder+'/right.png',
            'skyboxes/'+folder+'/left.png',
            'skyboxes/'+folder+'/top.png',
            'skyboxes/'+folder+'/bottom.png',
            'skyboxes/'+folder+'/front.png',
            'skyboxes/'+folder+'/back.png'
        ]

        # Creates the cubemap texture object
        self.cubemapTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubemapTexture)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # These are very important to prevent seams
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        # This might help with seams on some systems
        #glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)

        # Cycles through all the textures and attaches them to the cubemap object
        for i in range(0, len(facesCubemap)):
            textureImg = pygame.image.load(facesCubemap[i])
            width, height = textureImg.get_size()
            numberOfColorChannels = textureImg.get_bytesize()
            self.width = width
            self.height = height
            bytes = textureImg.get_buffer().raw
            if numberOfColorChannels == 4:
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X+i, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes)
            elif numberOfColorChannels == 3:
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X+i, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, bytes)
            elif numberOfColorChannels == 1:
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X+i, 0, GL_RGBA, width, height, 0, GL_RED, GL_UNSIGNED_BYTE, bytes)
            else:
                print("Cannot determine texture type.")
                exit()
        

    
    def draw(self, camera):
        # Since the cubemap will always have a depth of 1.0, we need that equal sign so it doesn't get discarded
        glDepthFunc(GL_LEQUAL)

        self.skyboxShader.activate()
        view = glm.mat4(1.0)
        projection = glm.mat4(1.0)
        # We make the mat4 into a mat3 and then a mat4 again in order to get rid of the last row and column
        # The last row and column affect the translation of the skybox (which we don't want to affect)
        view = glm.mat4(glm.mat3(glm.lookAt(camera.position, camera.position + camera.orientation, camera.up)))
        projection = glm.perspective(glm.radians(45.0), float(self.width) / float(self.height), 0.1, 100.0)
        glUniformMatrix4fv(glGetUniformLocation(self.skyboxShader.ID, "view"), 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(self.skyboxShader.ID, "projection"), 1, GL_FALSE, glm.value_ptr(projection))

        # Draws the cubemap as the last object so we can save a bit of performance by discarding all fragments
        # where an object is present (a depth of 1.0 will always fail against any object's depth value)
        glBindVertexArray(self.skyboxVAO)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubemapTexture)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        # Switch back to the normal depth function
        glDepthFunc(GL_LESS)