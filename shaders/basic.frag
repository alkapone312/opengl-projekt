#version 330 core

out vec4 FragColor;

in vec3 CurrentPos;
in vec3 Normal;
in vec2 TexCoord;

uniform sampler2D diffuse0;
uniform sampler2D specular0;
uniform sampler2D normal0;
uniform vec3 camPos;
uniform vec4 lightColor;
uniform vec3 lightPos;

vec4 pointLight() {
    vec3 normal = normalize(Normal);
    vec3 lightVec = lightPos - CurrentPos;
    float dist = length(lightVec);
    float a = 0.1;
    float b = 0.7;
    float specularLight = 0.5f;
    float intensity = 1.0f / (a * dist * dist + b * dist + 1.0f);
    vec3 lightDir = normalize(lightVec);
    vec3 viewDirection = normalize(camPos - CurrentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 16);
    float ambient = 0.2f;
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    return texture(diffuse0, TexCoord) * lightColor * (diffuse * intensity + ambient) + texture(specular0, TexCoord).r * specular * intensity;
}

vec4 directLight() {
    vec3 normal = normalize(Normal);
    vec3 lightDir = normalize(vec3(1.0f, 1.0f, 0.0f));
    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - CurrentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 16);
    
    float ambient = 0.2f;
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    return texture(diffuse0, TexCoord) * lightColor * (diffuse + ambient) + texture(specular0, TexCoord).r * specular;
}

vec4 spotLight() {
    float innerCone = 0.95f;
    float outerCone = 0.90f;

    vec3 lightDir = normalize(lightPos - CurrentPos);
    vec3 normal = normalize(Normal);

    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - CurrentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 16);
    
    float ambient = 0.2f;
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    float angle = dot(vec3(0.0f, -1.0f, 0.0f), -lightDir);
    float intensity = clamp((angle - outerCone) / (innerCone - outerCone), 0.0f, 1.0f);

    return texture(diffuse0, TexCoord) * (diffuse * intensity + ambient) + texture(specular0, TexCoord).r * specular * intensity * lightColor;
}

void main() {    
    FragColor = pointLight();
}