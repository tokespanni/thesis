from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from ctypes import sizeof, c_float, c_void_p, c_int

def c_matrix(matrix):
	matrixElements = []
	for i in range(16):
		matrixElements.append(matrix[i])
	return (matrixElements)

def genBuffers(light_sources, max_photons, light_size, lightsource_num):
	float_size = sizeof(c_float)
	int_size = sizeof(c_int)
	
	# generate VAO, VBO
	vaos = glGenVertexArrays(1)
	vbos = glGenBuffers(1)
	vertices = np.array([0,0,0],dtype = 'f')
	glBindVertexArray(vaos)
	glBindBuffer(GL_ARRAY_BUFFER, vbos)
	glBufferData(GL_ARRAY_BUFFER, float_size*3, vertices, GL_STREAM_DRAW)
	glEnableVertexAttribArray(0)
	glVertexAttribPointer(0, 3, GL_FLOAT, False, float_size*3, c_void_p(0 * float_size) )
	#glEnable(GL_CULL_FACE)
	
	lightSourceBuffer = glGenBuffers(1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, lightSourceBuffer)
	glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*light_size*lightsource_num, light_sources, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
	
	indices = np.arange(max_photons, dtype = 'i')
	emptyIndices = glGenBuffers(1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, emptyIndices)
	glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(c_int)*max_photons, indices, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
	
	positions = np.zeros(4*max_photons, dtype = 'f')
	input_pos = glGenBuffers(1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, input_pos)
	glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(4*max_photons), positions, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
	
	output_pos = glGenBuffers(1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, output_pos)
	glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(4*max_photons), positions, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
	
	photons = np.zeros(8*max_photons, dtype = 'f')
	photonBuffer = glGenBuffers(1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, photonBuffer)
	glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(8*max_photons), photons, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
	
	atomic = glGenBuffers(1)
	glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, atomic)
	glBufferData(GL_ATOMIC_COUNTER_BUFFER, int_size, np.array([1073741824+max_photons-1], dtype = 'l'), GL_DYNAMIC_DRAW)
	glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, 0)
	
	return vaos, vbos, lightSourceBuffer, emptyIndices, input_pos, output_pos, photonBuffer, atomic
	
def genFBO(fbo_created, framebuffer, fbo_texture):
	# if this is called from resize: clean up the previous resources
	if fbo_created == True:
		glDeleteFramebuffers(1, [framebuffer])
		glDeleteTextures([fbo_texture])
	# define the FBO
	framebuffer = glGenFramebuffers(1)
	glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)
	# setup render texture attachment
	fbo_texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, fbo_texture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 1024, 1024, 0, GL_RGBA, GL_FLOAT, None)
	glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, fbo_texture, 0)
	# check FBO completeness - should raise big fat red flag if this fails
	fbo_status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
	if fbo_status != GL_FRAMEBUFFER_COMPLETE:
		print "[BigFatRedFlag]", fbo_status
	# revert to default FBO
	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	fbo_created = True
	return fbo_created, framebuffer, fbo_texture
	
	#http://www.efg2.com/Lab/ScienceAndEngineering/Spectra.htm
	'''def waveLengthToRGB(wavelength):
		#390 to 750
		self.wavelength = 700
		gamma = 0.80
		maxIntensity = 255
		
		red, green, blue, factor = 0.0,0.0,0.0,0.0
		if wavelength >= 380 and wavelength < 440:
			red = -(wavelength - 440.0) / (440.0 - 380.0)
			green = 0.0
			blue =  1.0
		elif wavelength >= 440 and wavelength < 490:
			red = 0.0
			green = (wavelength - 440.0) / (490.0 - 440.0)
			blue = 1.0
		elif wavelength >= 490 and wavelength < 510:
			red = 0.0
			green = 1.0
			blue = -(wavelength - 510.0) / (510.0 - 490.0)
		elif wavelength >= 510 and wavelength < 580:
			red = (wavelength - 510.0) / (580.0 - 510.0)
			green = 1.0
			blue = 0.0
		elif wavelength >= 580 and wavelength < 645:
			red = 1.0
			green = -(wavelength - 645) / (645.0 - 580.0)
			blue = 0.0
		elif wavelength >= 645 and wavelength < 781:
			red = 1.0
			green = 0.0
			blue = 0.0
		else:
			red = 0.0
			green = 0.0
			blue = 0.0
		
		if wavelength >= 380 and wavelength < 420:
			factor = 0.3 + 0.7*(wavelength - 380.0) / (420.0 - 380.0)
		elif wavelength >= 420 and wavelength < 701:
			factor = 1.0
		elif wavelength > 701 and wavelength < 781:
			factor = 0.3 + 0.7*(780.0 - wavelength) / (780.0 - 700.0)
		else:
			factor = 0.0
		
		r = 0 if red == 0.0 else int(math.floor(maxIntensity * math.pow(red * factor, gamma)))
		g = 0 if green == 0.0 else int(math.floor(maxIntensity * math.pow(green * factor, gamma)))
		b = 0 if blue == 0.0 else int(math.floor(maxIntensity * math.pow(blue * factor, gamma)))
		
		return r, g, b'''