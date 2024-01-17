#version 330 core

out vec4 FragColor;

in vec3 CurrentPos;
in vec3 Normal;
in vec2 TexCoord;

uniform sampler2D diffuse0;
uniform sampler2D specular0;
uniform sampler2D normal0;
uniform vec3 camPos;

uniform int numPoint;
uniform int numDir;
uniform int numSpot;

struct DirLight {
    vec3 direction;
    vec4 color;
};  
uniform DirLight dirLight[1];

struct PointLight {    
    vec3 position;
    vec4 color;
    
    float constant;
    float linear;
    float quadratic;  
};
#define NR_POINT_LIGHTS 255  
uniform PointLight pointLights[NR_POINT_LIGHTS];

struct SpotLight {
    vec3 position;
    vec3 direction;
    vec4 color;

    float innerCone;
    float outerCone;
};
#define NR_SPOT_LIGHTS 255
uniform SpotLight spotLights[NR_SPOT_LIGHTS];

vec4 pointLight(PointLight light) {
    vec3 normal = normalize(Normal);
    vec3 lightVec = light.position - CurrentPos;
    float dist = length(lightVec);
    float a = light.quadratic;
    float b = light.linear;
    float c = light.constant;
    float specularLight = 0.5f;
    float intensity = 1.0f / (a * dist * dist + b * dist + c);
    vec3 lightDir = normalize(lightVec);
    vec3 viewDirection = normalize(camPos - CurrentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 8);
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    return texture(diffuse0, TexCoord) * light.color * (diffuse * intensity) + texture(specular0, TexCoord).r * specular * intensity;
}

vec4 directLight() {
    vec3 normal = normalize(Normal);
    vec3 lightDir = normalize(dirLight[0].direction);
    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - CurrentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 16);
    
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;

    return texture(diffuse0, TexCoord) * dirLight[0].color * (diffuse) + texture(specular0, TexCoord).r * specular;
}

vec4 spotLight(SpotLight light) {
    float innerCone = light.innerCone;
    float outerCone = light.outerCone;

    vec3 lightDir = normalize(light.position - CurrentPos);
    vec3 normal = normalize(Normal);

    float specularLight = 0.5f;
    vec3 viewDirection = normalize(camPos - CurrentPos);
    vec3 reflectionDirection = reflect(-lightDir, normal);
    float specAmount = pow(max(dot(viewDirection, reflectionDirection), 0.0f), 8);
    
    float diffuse = max(dot(normal, lightDir), 0.0f);
    float specular = specAmount * specularLight;


    float angle = dot(vec3(0.0f, -1.0f, 0.0f), -lightDir);
    float intensity = clamp((angle - outerCone) / (innerCone - outerCone), 0.0f, 0.2f);

    return texture(diffuse0, TexCoord) * (diffuse * intensity) + texture(specular0, TexCoord).r * specular * intensity * light.color;
}

vec4 ambientLight() {
    return texture(diffuse0, TexCoord) * 0.1f;
}

void main() {
    vec4 result = ambientLight();

    for(int i = 0 ; i < numDir; i++) {
        result += directLight();
    }
    
    for(int i = 0; i < numPoint; i++) {
        result += pointLight(pointLights[i])  / numPoint;
    }

    for(int i = 0; i < numSpot; i++) {
        result += spotLight(spotLights[i]);
    }
    
    FragColor = result;
}