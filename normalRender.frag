#version 430

in vec3 vs_out_col;
out vec4 fs_out_col;

void main()
{
	fs_out_col.xyz = vs_out_col;
}