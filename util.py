from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from ctypes import sizeof, c_float, c_void_p, c_int
import math

def c_matrix(matrix):
	matrixElements = []
	for i in range(16):
		matrixElements.append(matrix[i])
	return (matrixElements)

def genBuffers(light_sources, max_photons, lightsource_num, surface_params):
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
	glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*8*lightsource_num, light_sources, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
	
	indices = np.arange(max_photons, dtype = 'i')
	emptyIndices = glGenBuffers(1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, emptyIndices)
	glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(c_int)*max_photons, indices, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
	
	# pos.x		pos.y		time 		dummy
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
	
	surfaceParamsBuffer = glGenBuffers(1)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, surfaceParamsBuffer)
	glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*8, surface_params, GL_STREAM_DRAW)
	glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

	return vaos, vbos, lightSourceBuffer, emptyIndices, input_pos, output_pos, photonBuffer, atomic, surfaceParamsBuffer
	
def genFBO(fbo_created, framebuffer, fbo_texture, texw, texh):
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
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB16F, texw, texh, 0, GL_RGB, GL_FLOAT, None)
	glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, fbo_texture, 0)
	# check FBO completeness - should raise big fat red flag if this fails
	fbo_status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
	if fbo_status != GL_FRAMEBUFFER_COMPLETE:
		print "[BigFatRedFlag]", fbo_status
	# revert to default FBO
	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	fbo_created = True
	return fbo_created, framebuffer, fbo_texture
	
def concat_files_to_shader(begin, f, end):
	filename = begin.split('_')[0]
	filetype = begin.split('.')[1]
	with open(filename + '.' + filetype, 'w') as outfile:
		for fname in [begin, f, end]:
			with open(fname) as infile:
				outfile.write(infile.read())

def adjust(color, f):
	intensityMax = 255
	gamma = 0.8
	if color == 0:
		return 0
	else:
		return round(intensityMax * math.pow(color * f, gamma))
		
def wavelength_to_rgb(wl):
	if wl >= 380 and wl < 440:
		red = -(wl - 440)/(440.0 - 380.0)
		green = 0
		blue = 1.0
		
	if wl >= 440 and wl < 490:
		red = 0
		red = (wl - 440)/(490.0 - 440.0)
		blue = 1.0
		
	if wl >= 490 and wl < 510:
		red = 0
		green = 1.0
		blue = -(wl - 510)/(510.0 - 440.0)
		
	if wl >= 510 and wl < 580:
		red = (wl - 510)/(580.0 - 510.0)
		green = 1.0
		blue = 0
		
	if wl >= 580 and wl < 645:
		red = 1.0
		green = -(wl - 645)/(645.0 - 580.0)
		blue = 0
		
	if wl >= 645 and wl <= 780:
		red = 1.0
		green = 0
		blue = 0		
	
	if wl < 380 or wl > 780:
		red = 0
		green = 0
		blue = 0
		
	if wl >= 380 and wl < 420:
		f = 0.3 + 0.7 * (wl -380) / (420.0 - 380.0)
		
	if wl >= 420 and wl <= 700:
		f = 1.0
		
	if wl > 700 and wl <= 780:
		f = 0.3 + 0.7 * (780 - wl) / (780.0 - 700.0)
		
	if wl < 380 or wl > 780:
		f = 0.0
		
	r = adjust(red, f)
	g = adjust(green, f)
	b = adjust(blue, f)
	
	return [r, g, b]
