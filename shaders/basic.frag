#version 330 core

out vec4 FragColor;

in vec3 currentPos;
in vec3 normal;
in vec3 color;
in vec2 texCoord;

uniform sampler2D diffuse0;
uniform sampler2D specular0;
uniform vec3 camPos;
uniform vec4 lightColor;
uniform vec3 lightPos;

vec4 pointLight() {
    vec3 lightVec = lightPos - currentPos;
    float dist = length(lightVec);
    float a = 3;
    float b = 0.7;
    float intensity = 1.0f / (a * dist * dist + b * dist + 1.0f);
    vec3 lightDir = normalize(lightVec);
    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - currentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 16);
    
    float ambient = 0.2f;
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    return texture(diffuse0, texCoord) * lightColor * (diffuse * intensity + ambient) + texture(specular0, texCoord).r * specular * intensity;
}

vec4 directLight() {
    vec3 lightDir = normalize(vec3(1.0f, 1.0f, 0.0f));
    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - currentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 16);
    
    float ambient = 0.2f;
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    return texture(diffuse0, texCoord) * lightColor * (diffuse + ambient) + texture(specular0, texCoord).r * specular;
}

vec4 spotLight() {
    float innerCone = 0.95f;
    float outerCone = 0.90f;

    vec3 lightDir = normalize(lightPos - currentPos);
    
    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - currentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 16);
    
    float ambient = 0.2f;
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    float angle = dot(vec3(0.0f, -1.0f, 0.0f), -lightDir);
    float intensity = clamp((angle - outerCone) / (innerCone - outerCone), 0.0f, 1.0f);

    return texture(diffuse0, texCoord) * (diffuse * intensity + ambient) + texture(specular0, texCoord).r * specular * intensity * lightColor;
}

void main() {
    vec3 normalized = normalize(normal);
    
    FragColor = spotLight();
}