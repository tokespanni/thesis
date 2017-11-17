
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
	gl_Position = vec4(pos_trafo(gl_Position.xy), gl_Position.zw);
	if(photons[id].speed == vec2(0))
		gl_Position = vec4(-2,-2,0,1);
	power = photons[id].power;
	wavelength = photons[id].wavelength;
} 