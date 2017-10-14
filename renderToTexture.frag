#version 430

in vec3 col;
out vec4 color;
layout(location = 0) uniform vec3 rgb;

void main()
{
	//color = vec4(col,1);
	color = vec4(rgb,1);
}

/*
vec3 waveLenghtToRGB(int waveLenght)
{
	float factor;
	float red, green, blue;
	
	if (waveLenght >= 380 && waveLenght < 440)
	{
		red = -(waveLenght - 440) / (440 - 380);
		green = 0.0;
		blue = 1.0;
	}
	else if (waveLenght >= 440 && waveLenght < 490)
	{
		red = 0.0;
		green = (waveLenght - 440) / (490 - 440);
		blue = 1.0;
	}
	else if (waveLenght >= 490 && waveLenght < 510)
	{
		red = 0.0;
		green = 1.0;
		blue = -(waveLenght - 510) / (580 - 510);
	}
	else if (
}*/