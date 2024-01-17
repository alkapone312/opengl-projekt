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
        directLights = lights.getDirLights()
        pointLights = lights.getPointLights()
        spotLights = lights.getSpotLights()
        glUniform1i(glGetUniformLocation(model.shader.ID, "numDir"), len(directLights))
        glUniform1i(glGetUniformLocation(model.shader.ID, "numPoint"), len(pointLights))
        glUniform1i(glGetUniformLocation(model.shader.ID, "numSpot"), len(spotLights))
        for i in range(len(directLights)):
            glUniform3f(glGetUniformLocation(model.shader.ID, "dirLight[0].direction"), directLights[0].direction.x, directLights[0].direction.y, directLights[0].direction.z)
            glUniform4f(glGetUniformLocation(model.shader.ID, "dirLight[0].color"), directLights[0].color.x, directLights[0].color.y, directLights[0].color.z, directLights[0].color.w)
        for i in range(0, len(pointLights)):
            glUniform3f(glGetUniformLocation(model.shader.ID, "pointLights[" + str(i) + "].position"), pointLights[i].position.x, pointLights[i].position.y, pointLights[i].position.z)
            glUniform4f(glGetUniformLocation(model.shader.ID, "pointLights[" + str(i) + "].color"), pointLights[i].color.x, pointLights[i].color.y, pointLights[i].color.z, pointLights[i].color.w)
            glUniform1f(glGetUniformLocation(model.shader.ID, "pointLights[" + str(i) + "].quadratic"), pointLights[i].quadratic)
            glUniform1f(glGetUniformLocation(model.shader.ID, "pointLights[" + str(i) + "].linear"), pointLights[i].linear)
            glUniform1f(glGetUniformLocation(model.shader.ID, "pointLights[" + str(i) + "].constant"), pointLights[i].constant)
        for i in range(0, len(spotLights)):
            glUniform3f(glGetUniformLocation(model.shader.ID, "spotLights[" + str(i) + "].position"), spotLights[i].position.x, spotLights[i].position.y, spotLights[i].position.z)
            glUniform4f(glGetUniformLocation(model.shader.ID, "spotLights[" + str(i) + "].color"), spotLights[i].color.x, spotLights[i].color.y, spotLights[i].color.z, spotLights[i].color.w)
            glUniform3f(glGetUniformLocation(model.shader.ID, "spotLights[" + str(i) + "].direction"), spotLights[i].direction.x, spotLights[i].direction.y, spotLights[i].direction.z)
            glUniform1f(glGetUniformLocation(model.shader.ID, "spotLights[" + str(i) + "].innerCone"), spotLights[i].innerCone)
            glUniform1f(glGetUniformLocation(model.shader.ID, "spotLights[" + str(i) + "].outerCone"), spotLights[i].outerCone)
        modelMatrix = model.getModelMatrix()
        glUniformMatrix4fv(glGetUniformLocation(model.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(modelMatrix))

        if len(model.mesh.getIndices()) != 0:
            glDrawElements(GL_TRIANGLES, len(model.mesh.getIndices()), GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(GL_TRIANGLES, 0, len(model.mesh.getVertices() / 8))

        for texture in model.textures:
            texture.unbind()
