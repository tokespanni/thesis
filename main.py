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
		self.program = None
		self.photon_birth_program = None
		self.photon_simulation_program = None
		self.param_program = None
		self.camera = Camera()
		self.last_time = 0
		self.delta_time = 0
		
		self.max_photons = 1024*16
		self.photon_birth_count = 64
		
		#self.setMouseTracking(True)
		
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
		self.program = self.render_program("normalRender.vert", "normalRender.frag")
		self.debugProgram = self.render_program("debug.vert", "debug.frag")
		#self.param_program = self.render_program("parametricSurface.vert", "parametricSurface.frag") 
		self.genBuffers()
		glPointSize(3.0);
		self.texLoc = glGetUniformLocation( self.program, "texImage" )
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
		this_time = pygame.time.get_ticks()/1000.0;
		self.delta_time = (this_time - self.last_time)
		self.last_time = this_time
		
		self.camera.update(self.delta_time)
		
		glUseProgram(self.photon_birth_program)
		glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, self.atomic)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.posBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.speedBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.emptyIndices)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.lightSourceBuffer)
		glDispatchCompute(self.photon_birth_count,1,1)
		glUseProgram(0)
		
		glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT | GL_ATOMIC_COUNTER_BARRIER_BIT)
		
		glUseProgram(self.photon_simulation_program)
		glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, self.atomic)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.posBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.speedBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.emptyIndices)
		glUniform1f(0, self.delta_time)
		glDispatchCompute(self.max_photons, 1, 1)
		glUseProgram(0)
		
		glMemoryBarrier(GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT)
		glFinish()
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, self.atomic)
		atomicCountDebug = glGetBufferSubData(GL_ATOMIC_COUNTER_BUFFER,0,1*sizeof(c_int))
		asd = atomicCountDebug[3]*256*256*256+atomicCountDebug[2]*256*256 + atomicCountDebug[1]*256 +atomicCountDebug[0] - 1073741824
		print "atomicCountDebug = ", asd
		#render
		matWorld = Matrix4()
		matWorldIT = matWorld.inverse().transposed()
		mvp = self.camera.matViewProj * matWorld
			
		glUseProgram(self.program)
		
		glUniformMatrix4fv(0, 1, GL_FALSE, self.c_matrix(matWorld))
		glUniformMatrix4fv(4, 1, GL_FALSE, self.c_matrix(matWorldIT))
		glUniformMatrix4fv(8, 1, GL_FALSE, self.c_matrix(mvp))

		glClearColor(0.2, 0.3, 0.4, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.texID)
		glUniform1i(self.texLoc, 0)

		glBindVertexArray(self.vaos)
		
		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
		glBindVertexArray(0)
		glBindTexture(GL_TEXTURE_2D, 0)
		glUseProgram(0)
		
		glUseProgram(self.debugProgram)
		glBindVertexArray(self.debugVAO)
		glDrawArrays(GL_POINTS, 0, self.max_photons)
		glBindVertexArray(0)
		glUseProgram(0)
		
		
		self.update()
		
	def resizeGL(self, w, h):
		glViewport(0, 0, w-1, h-1)
	
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
		
		light_sources = np.array([0,0], dtype = 'f')
		self.lightSourceBuffer = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.lightSourceBuffer)
		glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(2), light_sources, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		
		indices = np.arange(self.max_photons, dtype = 'i')
		self.emptyIndices = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.emptyIndices)
		glBufferData(GL_SHADER_STORAGE_BUFFER, sizeof(c_int)*self.max_photons, indices, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		positions = np.zeros(2*self.max_photons, dtype = 'f')
		self.posBuffer = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.posBuffer)
		glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(2*self.max_photons), positions, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		speeds = np.zeros(2*self.max_photons, dtype = 'f')
		self.speedBuffer = glGenBuffers(1)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.speedBuffer)
		glBufferData(GL_SHADER_STORAGE_BUFFER, float_size*(2*self.max_photons), speeds, GL_STREAM_DRAW)
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
		
		self.debugVAO = glGenVertexArrays(1)
		glBindVertexArray(self.debugVAO)
		
		glBindBuffer(GL_ARRAY_BUFFER, self.posBuffer)
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0, 2, GL_FLOAT, False, float_size*2, c_void_p(0 * float_size) )
		
		glBindBuffer(GL_ARRAY_BUFFER, self.speedBuffer)
		glEnableVertexAttribArray(1)
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
	
		
	def keyPressEvent(self, e):
		self.camera.keyboardDown(e)
		if e.key() == Qt.Key_Escape:
			self.close()
		if e.key() == Qt.Key_C:
			self.camera.toCenter()
			
	def mousePressEvent(self, e):
		self.camera.click(e)
		
	def keyReleaseEvent(self,e):
		self.camera.keyboardUp(e)
			
	def mouseMoveEvent(self,e):
		self.camera.mouseMove(e, self.delta_time)
		
	def c_matrix(self, matrix):
		matrixElements = []
		for i in range(16):
			matrixElements.append(matrix[i])
		return (matrixElements)
		
if __name__ == '__main__':
	pygame.init()
	app = QtWidgets.QApplication(["PyQt OpenGL speed benchmark"])
	widget = Main()
	widget.show()
	app.exec_()
	print np.mean( widget.times )
	