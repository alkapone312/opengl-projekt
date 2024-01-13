#version 330 core

layout (location=0) in vec3 aPos;
layout (location=1) in vec3 aNormal;
layout (location=2) in vec2 aTex;

out vec3 CurrentPos;
out vec3 Normal;
out vec2 TexCoord;

uniform mat4 camMatrix;
uniform mat4 model;

void main() {
    CurrentPos = vec3(model * vec4(aPos, 1.0f));
    Normal = aNormal;
    TexCoord = aTex;
    gl_Position = camMatrix * model * vec4(CurrentPos, 1.0);
}