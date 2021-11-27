#version 460

layout(location = 0) out vec4 fragColor;

uniform int clock;

in vec3 mycolor;
in vec3 mynormal;

void main(){
  if (mod(clock/10, 2) == 0) {
    fragColor = vec4(mycolor.xyz * mynormal, 1.0f);
  }else {
    fragColor = vec4(mycolor.zxy * mynormal, 1.0f);
  }
}
