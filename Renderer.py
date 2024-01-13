import glm
from OpenGL.GL import *

class Renderer:
    def __init__(self):
        pass

    def render(self, model, lights, camera):
        model.shader.activate()
        model.mesh.vertexArray.bind()
        numDiffuse = 0
        numSpecular = 0
        numNormal = 0
        for i in range(0, len(model.textures)):
            num = ""
            type = model.textures[i].texType
            if type == "diffuse":
                num = numDiffuse
                numDiffuse += 1
            elif type == "specular":
                num = numSpecular
                numSpecular += 1
            elif type == "normal":
                num = numNormal
                numNormal += 1
            model.textures[i].texUni(model.shader, type + str(num), i)
            model.textures[i].bind()
        glUniform3f(
            glGetUniformLocation(model.shader.ID, "camPos"), 
            camera.position.x, 
            camera.position.y, 
            camera.position.z
        )
        camera.matrix(model.shader, "camMatrix")
        glUniform4f(glGetUniformLocation(model.shader.ID, "lightColor"), lights.color.x, lights.color.y, lights.color.z, lights.color.w)
        glUniform3f(glGetUniformLocation(model.shader.ID, "lightPos"), lights.position.x, lights.position.y, lights.position.z)
        modelMatrix = model.getModelMatrix()
        glUniformMatrix4fv(glGetUniformLocation(model.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(modelMatrix))

        if len(model.mesh.getIndices()) != 0:
            glDrawElements(GL_TRIANGLES, len(model.mesh.getIndices()), GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(GL_TRIANGLES, 0, len(model.mesh.getVertices() / 8))