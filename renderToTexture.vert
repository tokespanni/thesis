#version 430

struct photon
{
	vec3 color;
	float birthTime;
	vec2 speed;
	float wavelength;
	float birthPower;
};
restrict readonly layout(std430, binding = 1) buffer posBuffer1
{
	vec4 pos1[];
};
restrict readonly layout(std430, binding = 2) buffer posBuffer2
{
	vec4 pos2[];
};
restrict layout(std430, binding = 3) buffer photonBuffer
{
	photon photons[];
};

layout(location = 0) in vec2 dir;
out vec3 col;
out float time;
out float power;
out float wavelength;

void main()
{
	if (gl_VertexID % 2 == 0)
	{
		gl_Position = vec4(pos1[gl_VertexID/2].xy, 0, 1);
		col = photons[gl_VertexID/2].color;
		time = pos1[gl_VertexID/2].z;
		power = photons[gl_VertexID/2].birthPower;
		wavelength = photons[gl_VertexID/2].wavelength;
	}
	else
	{
		gl_Position = vec4(pos2[(gl_VertexID - 1)/2].xy, 0, 1);
		col = photons[(gl_VertexID - 1)/2].color;
		time = pos1[(gl_VertexID - 1)/2].z;
		power = photons[(gl_VertexID - 1)/2].birthPower;
		wavelength = photons[(gl_VertexID - 1)/2].wavelength;

	}
} 