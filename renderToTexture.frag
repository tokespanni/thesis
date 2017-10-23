#version 430

in vec3 col;
in float time;
in float power;

out vec4 color;

void main()
{
	color = vec4(col,1)*1/ time * power * 1000;
}
