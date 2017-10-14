#version 430

in vec3 vs_out_col;
out vec4 fs_out_col;
in vec2 vs_out_tex0;

uniform sampler2D texImage;

void main()
{
	fs_out_col.xyz = vs_out_col;
	fs_out_col = vec4(vs_out_col, 1) * texture(texImage, vs_out_tex0.st);
}