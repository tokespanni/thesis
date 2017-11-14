#version 430

struct photon
{
	vec3 color;
	float birthTime;
	vec2 speed;
	float wavelength;
	float power;
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
out float time;
out float power;
out float wavelength;
