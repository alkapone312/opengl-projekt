import numpy as np
import math

class VerticesTransformer:
    def __init__(self, vertices, vertexLength):
        self.vertices = vertices
        self.vertexLength = vertexLength

    def translate(self, x, y, z):
        newVertices = []
        for i in range(0, len(self.vertices)):
            if i%self.vertexLength == 0:
                newVertices.append(self.vertices[i] + x) 
                newVertices.append(self.vertices[i+1] + y) 
                newVertices.append(self.vertices[i+2] + z) 
            elif i%self.vertexLength > 2:
                newVertices.append(self.vertices[i])

        return np.array(newVertices, dtype='float32')

    def rotate(self, x, y, z):
        unit = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        xRotation = unit
        yRotation = unit
        zRotation = unit
        rotation = unit

        x = np.deg2rad(x)
        y = np.deg2rad(y)
        z = np.deg2rad(z)

        if x != 0:
            xRotation = np.array([
                [1, 0, 0],
                [0, math.cos(x), -math.sin(x)],
                [0, math.sin(x), math.cos(x)],
            ])
            rotation = rotation.dot(xRotation)
        if y != 0:
            yRotation = np.array([
                [math.cos(y), 0, math.sin(y)],
                [0, 1, 0],
                [-math.sin(y), 0, math.cos(y)]
            ])
            rotation = rotation.dot(yRotation)
        if z != 0:
            zRotation = np.array([
                [math.cos(z), -math.sin(z), 0],
                [math.sin(z), math.cos(z), 0],
                [0, 0, 1]
            ])
            rotation = rotation.dot(zRotation)
        newVertices = []
        for i in range(0, len(self.vertices)):
            if i%self.vertexLength == 0:
                newVertices.extend(rotation.dot(
                        (self.vertices[i], self.vertices[i+1], self.vertices[i+2])
                ))
                newVertices.extend(rotation.dot(
                        (self.vertices[i+3], self.vertices[i+4], self.vertices[i+5])
                ))
            elif i%self.vertexLength > 5:
                newVertices.append(self.vertices[i])

        return np.array(newVertices, dtype='float32')

    def scale(self, x, y, z):
        newVertices = []
        for i in range(0, len(self.vertices)):
            if i%self.vertexLength == 0:
                newVertices.append(self.vertices[i] * x) 
                newVertices.append(self.vertices[i+1] * y) 
                newVertices.append(self.vertices[i+2] * z) 
            elif i%self.vertexLength > 2:
                newVertices.append(self.vertices[i])

        return np.array(newVertices, dtype='float32')