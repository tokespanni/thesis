#version 430

//in vec3 vs_out_col;
//in vec2 vs_out_tex0;
out vec4 fs_out_col;

in block
{
	vec3	pos;
	vec3	n;
	vec2	uv;
} In;

uniform sampler2D texImage;

uniform vec3 light = vec3(5);
uniform vec3 eye = vec3(3);

void main()
{
	vec3 col = vec3(0);
	//ambient
	col+= vec3(0.1,0.2,0.3);
	
	//diffuse
	vec3 n = normalize(In.n);
	vec3 toLight = normalize(light - In.pos);
	float di = clamp(dot(n,toLight),0,1);
	col+= di*vec3(0.7,0.6,0.5);
	
	//texture
	col*= texture(texImage, In.uv).xyz;
	
	//specular
	if( di > 0)
	{
		vec3 h = normalize(n + toLight);
		vec3 toEye = normalize(eye - In.pos);
		col += clamp(pow(dot(toEye, h),100),0,1)*vec3(1,1,1);
	}
	
	fs_out_col.xyz = col;
}