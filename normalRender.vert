#version 430

layout(location = 0) in vec3 vs_in_pos;
layout(location = 1) in vec3 vs_in_col;
layout(location = 2) in vec2 vs_in_tex0;


out vec3 vs_out_col;
out vec2 vs_out_tex0;

layout(location = 0) uniform mat4 world;
layout(location = 4) uniform mat4 worldIT;
layout(location = 8) uniform mat4 mvp;

void main()
{
	gl_Position = mvp * vec4( vs_in_pos, 1);
	vs_out_col = vs_in_col;
	vs_out_tex0 = vs_in_tex0;
}