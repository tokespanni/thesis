#version 430

layout(location = 0) in vec3 vs_in_pos;

out block
{
	vec3 pos;
} Out;


layout(location = 0) uniform mat4 world;
layout(location = 4) uniform mat4 worldIT;
layout(location = 8) uniform mat4 mvp;

void main()
{
	//gl_Position = mvp * vec4( vs_in_pos, 1);
	Out.pos = vs_in_pos;
}