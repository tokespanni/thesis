from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtOpenGL import *
import numpy as np
import time
from ctypes import sizeof, c_float, c_void_p, c_int
import math
from camera import *
import sys
sys.path.insert(0, 'C:/Users/Panni/thesis_in_Python/pyeuclid')
from euclid import *
import pygame.time
import pygame

class Main(QGLWidget):
	def __init__(self, parent = None):
		
		super(Main, self).__init__(parent)
		self.setGeometry( 30,30, 640, 480 )
		self.fps_last_time = 0
		self.fps_frame_count = 0		
		self.times = []
		self.texture_program = None
		self.photon_birth_program = None
		self.photon_simulation_program = None
		self.param_program = None
		self.camera = Camera()
		self.last_time = 0
		self.delta_time = 0
		
		self.frame_count = 0
		self.max_photons = 1024*512
		self.photon_birth_count = 1024
		#390 to 750
		self.wavelength = 700
		self.fbo_created = False
		self.lightsource_num = 2
		self.total_light_power = 0
				
	def compute_program(self, shader_file):
		program = glCreateProgram()
		compute_shader_id = self.load_and_compile_shader(GL_COMPUTE_SHADER, shader_file)
		glAttachShader(program, compute_shader_id)
		glLinkProgram(program)
		message = glGetProgramInfoLog(program)
		if message:
			print("[Shader linking failed]")
			print(message)
		glDeleteShader(compute_shader_id)
		glUseProgram(0)
		return program
		
	def render_program(self, vertex_file, fragment_file):
		program = glCreateProgram()
		vertex_shader_id    = self.load_and_compile_shader(GL_VERTEX_SHADER, vertex_file)
		fragment_shader_id  = self.load_and_compile_shader(GL_FRAGMENT_SHADER, fragment_file)
		glAttachShader(program, vertex_shader_id)
		glAttachShader(program, fragment_shader_id)
		glLinkProgram(program)
		message = glGetProgramInfoLog(program)
		if message:
			print("[Shader linking failed]")
			print(message)
		# free up the now-unnecessary shader binaries
		glDeleteShader(vertex_shader_id)
		glDeleteShader(fragment_shader_id)
		glUseProgram(0)
		return program
		
	def initializeGL(self):
		print( "Running OpenGL %s.%s" % (glGetInteger(GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION)) )
		self.photon_birth_program = self.compute_program("birthOfPhotons.compute")
		self.photon_simulation_program = self.compute_program("simulationOfPhotons.compute")
		self.param_program = self.render_program("parametricSurface.vert", "parametricSurface.frag")
		self.texture_program = self.render_program("renderToTexture.vert", "renderToTexture.frag")
		self.genBuffers()
		glPointSize(3.0);
		self.texLoc = glGetUniformLocation( self.param_program, "texImage" )
		self.texID = self.loadTexture()
		
	#render
	def paintGL(self):
		
		# measure FPS
		self.fps_frame_count += 1
		self.fps_delta_time = abs( time.time() - self.fps_last_time )
		if self.fps_delta_time >= 1:
			if self.fps_frame_count:
				self.setWindowTitle( str(1000.0*float(self.fps_delta_time)/self.fps_frame_count) + " ms, " + str(self.fps_frame_count) + " FPS"  )
				self.times.append( self.fps_frame_count )
			self.fps_frame_count = 0
			self.fps_last_time = time.time()
		
		#update
		this_time = pygame.time.get_ticks()/1000.0
		self.delta_time = (this_time - self.last_time)
		self.last_time = this_time
		
		self.camera.update(self.delta_time)
		self.frame_count += 1
		
		glUseProgram(self.photon_birth_program)
		glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, self.atomic)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.photonBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.emptyIndices)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.lightSourceBuffer)
		glUniform1f(0, pygame.time.get_ticks()/1000.0)
		glUniform1i(1, self.photon_birth_count)
		glUniform1i(2, self.lightsource_num)
		for i in range(self.lightsource_num):
			self.total_light_power += self.light_sources[i*4 + 2] 
		glUniform1f(3, self.total_light_power)
		print "photon_birth_program"
		glDispatchCompute(self.photon_birth_count,1,1)
		glFinish()
		print "Done"
		glUseProgram(0) 
		glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT | GL_ATOMIC_COUNTER_BARRIER_BIT)
		
		glUseProgram(self.photon_simulation_program)
		glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, self.atomic)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.photonBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.emptyIndices)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.output_pos)
		glUniform1f(0, self.delta_time)
		glUniform1f(1, pygame.time.get_ticks()/1000.0)
		print "photon_simulation_program"
		glDispatchCompute(self.max_photons, 1, 1)
		glFinish()
		print "Done"
		glUseProgram(0)
		glMemoryBarrier(GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT)
		glFinish()
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, self.atomic)
		atomicCountDebug = glGetBufferSubData(GL_ATOMIC_COUNTER_BUFFER,0,1*sizeof(c_int))
		asd = atomicCountDebug[3]*256*256*256+atomicCountDebug[2]*256*256 + atomicCountDebug[1]*256 +atomicCountDebug[0] - 1073741824
		print "atomicCountDebug = ", asd
		
		#render
		
		glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
		glViewport(0,0,1024,1024)
		glUseProgram(self.texture_program)
		
		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT)		
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.output_pos)
		rgb = self.waveLengthToRGB(self.wavelength)
		glUniform3f(0, rgb[0], rgb[1], rgb[2])
		glBindVertexArray(0)
		glDrawArrays(GL_LINES, 0, self.max_photons*2)
		glBindVertexArray(0)
		self.input_pos, self.output_pos = self.output_pos, self.input_pos
		glUseProgram(0)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		glViewport(0,0, self.size().width(), self.size().height())
		
		
		glUseProgram(self.param_program)
		matWorld = Matrix4()
		matWorldIT = matWorld.inverse().transposed()
		mvp = self.camera.matViewProj * matWorld
		
		glUniformMatrix4fv(0, 1, GL_FALSE, self.c_matrix(matWorld))
		glUniformMatrix4fv(4, 1, GL_FALSE, self.c_matrix(matWorldIT))
		glUniformMatrix4fv(8, 1, GL_FALSE, self.c_matrix(mvp))

		glClearColor(0.2, 0.3, 0.4, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
		glUniform1i(self.texLoc, 0)

		glBindVertexArray(self.vaos)
		
		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
		glBindVertexArray(0)
		glBindTexture(GL_TEXTURE_2D, 0)
		glUseProgram(0)
		
		self.update()
		
	def resizeGL(self, w, h):
		glViewport(0, 0, w-1, h-1)
		self.genFBO()
	
	def closeEvent(self, event):
		print "end"
		#delete stuff
	
	def load_and_compile_shader(self, shader_type, name):
		source_code = None
		with open(name) as f:
			# in PyOpenGL implementation glShaderSource expects a list of strings
			source_code = f.readlines()
		
		shader_id = glCreateShader(shader_type)
		glShaderSource(shader_id, source_code)
		glCompileShader(shader_id)
		
		# get debug info
		message = glGetShaderInfoLog(shader_id)
		if message:
			print("[Shader compilation failed]")
			print(message)
		
		return shader_id
		
	
	def genBuffers(self):
		# generate VAO, VBO
		self.vaos = glGenVertexArrays(1)
		self.vbos = glGenBuffers(1)
		
		float_size = sizeof(c_float)
		int_size = sizeof(c_int)
		
		#    x, y, z,    r, g, b,     s, t
		vertices = np.array( [
			-1, 0, -1,  1, 0, 0,	 0, 0,
			-1, 0,  1,  0, 1, 0,     0, 1,
			 1, 0, -1,  0, 0, 1,	 1, 0,
			 1, 0,  1,  1, 1, 1, 	 1, 1,
		
		], dtype = 'f')
		
		glBindVertexArray(self.vaos)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbos)
		glBufferData(GL_ARRAY_BUFFER, float_size*(3+3+2)*4, vertices, GL_STREAM_DRAW)
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0, 3, GL_FLOAT, False, float_size*(3+3+2), c_void_p(0 * float_size) )
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(1, 3, GL_FLOAT, False, float_size*(3+3+2), c_void_p(3 * float_size) )
		glEnableVertexAttribArray(2)
		glVertexAttribPointer(2, 2, GL_FLOAT, False, float_size*(3+3+2), c_void_p(6 * float_size) )
		
		#glEnable(GL_CULL_FACE)
		
		self.vao_for_fbo = glGenVertexArrays(1)
		
		self.light_sources = np.array([-0.5, -0.5,5,0,0.5,0.5,5,0], dtype = 'f')
		self.lightSourceBuffer = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.lightSourceBuffer)
		glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*4*self.lightsource_num, self.light_sources, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		indices = np.arange(self.max_photons, dtype = 'i')
		self.emptyIndices = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.emptyIndices)
		glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(c_int)*self.max_photons, indices, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		positions = np.zeros(2*self.max_photons, dtype = 'f')
		self.input_pos = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.input_pos)
		glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(2*self.max_photons), positions, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		self.output_pos = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.output_pos)
		glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(2*self.max_photons), positions, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		photons = np.zeros(8*self.max_photons, dtype = 'f')
		self.photonBuffer = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.photonBuffer)
		glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(8*self.max_photons), photons, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		self.debugVAO = glGenVertexArrays(1)
		glBindVertexArray(self.debugVAO)
		
		glBindBuffer(GL_ARRAY_BUFFER, self.photonBuffer)
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(1, 2, GL_FLOAT, False, float_size*2, c_void_p(0 * float_size) )
		
		self.atomic = glGenBuffers(1)
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, self.atomic)
		glBufferData(GL_ATOMIC_COUNTER_BUFFER, int_size, np.array([1073741824+self.max_photons-1], dtype = 'l'), GL_DYNAMIC_DRAW)
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, 0)
		
	def loadTexture(self):
		textureSurface = pygame.image.load('borisz.png')
		textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
		width = textureSurface.get_width()
		height = textureSurface.get_height()

		glEnable(GL_TEXTURE_2D)
		texid = glGenTextures(1)

		glBindTexture(GL_TEXTURE_2D, texid)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
					 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

		return texid
		
	def genFBO(self):
		# if this is called from resize: clean up the previous resources
		if self.fbo_created == True:
			glDeleteFramebuffers(1, [self.framebuffer])
			glDeleteTextures([self.fbo_texture])
	
		# define the FBO
		self.framebuffer = glGenFramebuffers(1)
		glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
	
		# 1. setup render texture attachment
		self.fbo_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 1024, 1024, 0, GL_RGBA, GL_FLOAT, None)
		glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_texture, 0)
		
		# 3. check FBO completeness - should raise big fat red flag if this fails
		fbo_status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
		if fbo_status != GL_FRAMEBUFFER_COMPLETE:
			print "[BigFatRedFlag]"
	
		# revert to default FBO
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
	
		self.fbo_created = True
		
	def keyPressEvent(self, e):
		self.camera.keyboardDown(e)
		if e.key() == Qt.Key_Escape:
			self.close()
		if e.key() == Qt.Key_Plus:
			self.wavelength = min(self.wavelength + 1, 750)
		if e.key() == Qt.Key_Minus:
			self.wavelength = max(self.wavelength - 1, 390)

	def mousePressEvent(self, e):
		self.camera.click(e)
		
	def keyReleaseEvent(self,e):
		self.camera.keyboardUp(e)
			
	def mouseMoveEvent(self,e):
		self.camera.mouseMove(e, self.delta_time)
	
	def wheelEvent(self,e):
		self.camera.mouseWheel(e.angleDelta().y()/120)
		
	def c_matrix(self, matrix):
		matrixElements = []
		for i in range(16):
			matrixElements.append(matrix[i])
		return (matrixElements)
		
	#http://www.efg2.com/Lab/ScienceAndEngineering/Spectra.htm
	def waveLengthToRGB(self, wavelength):
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
		
		return r, g, b
		
if __name__ == '__main__':
	pygame.init()
	app = QtWidgets.QApplication(["PyQt OpenGL speed benchmark"])
	widget = Main()
	widget.show()
	app.exec_()
	print np.mean( widget.times )
	