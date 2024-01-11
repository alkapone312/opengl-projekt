#version 330 core

out vec4 FragColor;

in vec3 color;
in vec2 texCoord;

in vec3 normal;
in vec3 currentPos;

uniform vec3 camPos;
uniform sampler2D tex0;
uniform vec4 lightColor;
uniform vec3 lightPos;

void main() {
    vec3 normalized = normalize(normal);
    vec3 lightDir = normalize(lightPos - currentPos);
    
    float ambient = 0.2f;
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - currentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 8);
    float specular = specAmount * specularLight;

    FragColor = texture(tex0, texCoord) * lightColor * (diffuse + ambient + specular);
}