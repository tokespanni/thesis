#version 430

out vec4 fs_out_col;

in block
{
	vec3	pos;
	vec3	n;
	vec2	uv;
} In;

uniform sampler2D texImage;

uniform vec3 light = vec3(10);
layout(location = 12) uniform vec3 eye;


float collision_f(vec2 p)
{
	return 0.9 - length(p);
}

void main()
{
	vec3 col = vec3(0);
	//ambient
	if(collision_f(2*In.uv-1) < 0)
		col += vec3(0.3);
	else
		col+= vec3(0.02,0.03,0.04);
	
	//diffuse
	vec3 n = normalize(In.n);
	vec3 toLight = normalize(light - In.pos);
	float di = clamp(dot(n,toLight),0,1000);
	if(collision_f(2*In.uv-1) < 0)
		col+= di*vec3(0.6);
	else
		col+= di*vec3(0.15);
	
	//texture
	col += 1.5*texture(texImage, In.uv).xyz;
	
	//specular
	if( di > -1)
	{
		vec3 toEye = normalize(eye - In.pos);
		vec3 h = normalize(toEye + toLight);
		col += pow(clamp(dot(n, h),0,2),100)*vec3(1);
	}
	
	fs_out_col.xyz = (col*col + 0.3*col)/(col*col+0.33*col+0.2); //HDR 
	
}