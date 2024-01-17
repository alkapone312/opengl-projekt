from OpenGL.GL import *

class Shader:
    def __init__(self, vertexFile = 'shaders/basic.vert', fragmentFile = 'shaders/basic.frag'):
        vertexShaderSrc = open(vertexFile, 'r').read()
        fragmentShaderSrc = open(fragmentFile, 'r').read()

        # create vertex shader
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, vertexShaderSrc)
        glCompileShader(vertexShader)

        # create fragment shader
        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, fragmentShaderSrc)
        glCompileShader(fragmentShader)

        # compile shaders to program
        self.ID = glCreateProgram()
        glAttachShader(self.ID, vertexShader)
        glAttachShader(self.ID, fragmentShader)
        glLinkProgram(self.ID)

        # delete unused shaders
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)

    def activate(self):
        glUseProgram(self.ID)
        
    def delete(self):
        glDeleteProgram(self.ID)