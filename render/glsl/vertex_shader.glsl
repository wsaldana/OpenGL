#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor;
layout (location = 2) in vec3 normals;

uniform mat4 matrix;

out vec3 mycolor;
out vec3 mynormal;

void main(){
  gl_Position = matrix * vec4(position.xyz, 1);
  mycolor = ccolor;
  mynormal = normals;
}
