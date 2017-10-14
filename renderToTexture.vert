#version 430


restrict readonly layout(std430, binding = 1) buffer posBuffer1
{
	vec2 pos1[];
};
restrict readonly layout(std430, binding = 2) buffer posBuffer2
{
	vec2 pos2[];
};

layout(location = 0) in vec2 dir;
out vec3 col;

void main()
{
	col = vec3(1,1,0);
	if (gl_VertexID % 2 == 0)
	{
		gl_Position = vec4(pos1[gl_VertexID/2], 0, 1);
	}
	else
	{
		gl_Position = vec4(pos2[(gl_VertexID - 1)/2], 0, 1);
	}
} 