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

void main()
{
	int id;
	if (gl_VertexID % 2 == 0)
	{
		id = gl_VertexID/2;
		gl_Position = vec4(pos1[id].xy, 0, 1);
		time = pos1[id].z;
	}
	else
	{
		id = (gl_VertexID - 1)/2;
		gl_Position = vec4(pos2[id].xy, 0, 1);
		time = pos2[id].z;
	}
	if(photons[id].speed == vec2(0))
		gl_Position = vec4(-2,-2,0,1);
	power = photons[id].power;
	wavelength = photons[id].wavelength;
} 