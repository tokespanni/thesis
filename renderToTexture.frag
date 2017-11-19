#version 430

in vec3 geom_out_color;

out vec4 color;

void main()
{
	color = vec4(geom_out_color, 1);
}



