#version 430

in vec3 col;
in float time;
in float power;
in float wavelength;

out vec4 color;

float adjust(float color, float factor)
{
	float gamma = 0.80;
	float intensityMax = 255;
	
	if(color == 0)
	{
		return 0;
	}
	else
	{
		return intensityMax * pow(color * factor, gamma);
	}
}

vec3 wavelengthToRGB(float wavelength)
{
	
	float red, green, blue;
	float factor;
	if (wavelength >= 380 && wavelength < 440)
	{
		red = -(wavelength - 440.0) / (440.0 - 380.0);
		green = 0.0;
		blue = 1.0;
	}
	if (wavelength >= 440 && wavelength < 490)
	{
		red = 0.0;
		green = (wavelength - 440.0) / (490.0 - 440.0);
		blue = 1.0;		
	}
	if (wavelength >= 490 && wavelength < 510)
	{
		red = 0.0;
		green = 1.0;
		blue = -(wavelength - 510.0) / (510.0 - 490.0);
	}
	if (wavelength >= 510 && wavelength < 580)
	{
		red = (wavelength - 510.0) / (580.0 - 510.0);
		green = 1.0;
		blue = 0.0;
	}		
	if (wavelength >= 580 && wavelength < 645)
	{
		red = 1.0;
		green = -(wavelength - 645.0) / (645.0 - 580.0);
		blue = 0.0;
	}
	if (wavelength >= 645 && wavelength <= 780)
	{
		red = 1.0;
		green = 0.0;
		blue = 0.0;
	}
	if (wavelength < 380 || wavelength > 780)
	{
		red = 0.0;
		green = 0.0;
		blue = 0.0;
	}
	
	if (wavelength >= 380 && wavelength<420)
	{
		factor = 0.3 + 0.7 * (wavelength - 380.0) / (420.0 - 380.0);
	}
	if (wavelength >= 420 && wavelength<=700)
	{
		factor = 1.0;
	}
	if (wavelength >= 700 && wavelength<=780)
	{
		factor = 0.3 + 0.7 * (780.0 - wavelength) / (780.0 - 700.0);
	}
	if (wavelength <= 380 || wavelength >=780)
	{
		factor = 0.0;
	}
	
	float r = adjust(red, factor);
	float g = adjust(green, factor);
	float b = adjust(blue, factor);
	
	return vec3(r,g,b) / 255.0;
}


void main()
{
	color = vec4(wavelengthToRGB(wavelength), 1) * power * 1000;
}



