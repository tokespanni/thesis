#version 430

layout(location = 0) in vec2 pos;
layout(location = 1) in vec2 dir;
out vec3 col;

void main()
{
	col = vec3(dir,0);
	gl_Position = vec4(pos,0,1);
}