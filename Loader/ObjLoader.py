import os
import numpy
from Model.Model import Model
from Model.Mesh import Mesh

class ObjLoader:
    def __init__(self):
        pass

    def load(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        dirname = os.path.dirname(filename)

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords))

        return self.generateModel()
    
    def generateModel(self):
        finalVertices = []
        for face in self.faces:
            vertices, normals, texture_coords = face
            for i in range(len(vertices)):
                finalVertices.extend(self.vertices[vertices[i] - 1])
                finalVertices.extend(self.normals[normals[i] - 1])
                finalVertices.extend(self.texcoords[texture_coords[i] - 1])

        return Mesh(numpy.array(finalVertices, dtype='float32'))