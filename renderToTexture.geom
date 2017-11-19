#version 430

layout(points) in;
layout(line_strip, max_vertices=2) out;

in vec3 vs_out_col[];
in vec2 vs_out_speed[];

out vec3 geom_out_color;

restrict readonly layout(std430, binding = 1) buffer posBuffer1
{
	vec4 pos1[];
};
restrict readonly layout(std430, binding = 2) buffer posBuffer2
{
	vec4 pos2[];
};

void main()
{
	if(vs_out_speed[0] == vec2(0,0)) return;
	
	int index = gl_PrimitiveIDIn;
	
	vec2 p1 = pos1[index].xy;
	vec2 p2 = pos2[index].xy;
		
	vec2 pt = vec2(floor(p1.x), 0);
	vec2 p1_out = (p1-pt)*2-1;
	vec2 p2_out = (p2-pt)*2-1;
		
	gl_Position = vec4(p1_out,0,1);
	geom_out_color = vs_out_col[0] / pos1[index].z;
	EmitVertex();
	
	geom_out_color = vs_out_col[0] / pos2[index].z;
	gl_Position = vec4(p2_out,0,1);
	EmitVertex();
	
	
	EndPrimitive();
}