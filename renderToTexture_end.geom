	
	gl_Position = vec4(p1_out,0,1);
	geom_out_color = vs_out_col[0] / pos1[index].z;
	EmitVertex();
	
	geom_out_color = vs_out_col[0] / pos2[index].z;
	gl_Position = vec4(p2_out,0,1);
	EmitVertex();
	
	
	EndPrimitive();
}