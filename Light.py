import numpy
from Shader import Shader
from OpenGL.GL import *


class Light:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.vertices = numpy.array([
            -0.1, -0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
            -0.1, -0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
             0.1, -0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
             0.1, -0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
            -0.1,  0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
            -0.1,  0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
             0.1,  0.1, -0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
             0.1,  0.1,  0.1,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
        ], dtype="float32")
        self.indices = numpy.array([
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

    def setColor(self, color):
        self.color = color
    
    def setPosition(self, position):
        self.position = position
