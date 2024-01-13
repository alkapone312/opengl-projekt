from OpenGL.GL import *

class Renderer:
    def __init__(self):
        pass

    def render(self, mesh, shader, textures, light, camera):
        shader.activate()
        mesh.vertexArray.bind()
        numDiffuse = 0
        numSpecular = 0
        numNormal = 0
        for i in range(0, len(textures)):
            num = ""
            type = textures[i].texType
            if type == "diffuse":
                num = numDiffuse
                numDiffuse += 1
            elif type == "specular":
                num = numSpecular
                numSpecular += 1
            elif type == "normal":
                num = numNormal
                numNormal += 1
            textures[i].texUni(shader, type + str(num), i)
            textures[i].bind()
        glUniform3f(
            glGetUniformLocation(shader.ID, "camPos"), 
            camera.position.x, 
            camera.position.y, 
            camera.position.z
        )
        camera.matrix(shader, "camMatrix")
        glUniform4f(glGetUniformLocation(shader.ID, "lightColor"), light.color.x, light.color.y, light.color.z, light.color.w)
        glUniform3f(glGetUniformLocation(shader.ID, "lightPos"), light.position.x, light.position.y, light.position.z)

        glDrawElements(GL_TRIANGLES, len(mesh.getIndices()), GL_UNSIGNED_INT, None)
        pass