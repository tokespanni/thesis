from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtOpenGL import *
import numpy as np
from numpy import linalg as LA
import time
from ctypes import sizeof, c_float, c_void_p
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
		self.camera = Camera()
		self.last_time = 0
		self.delta_time = 0
		#self.setMouseTracking(True)

	def initializeGL(self):
		print( "Running OpenGL %s.%s" % (glGetInteger(GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION)) )
		
		self.program = glCreateProgram()
		vertex_shader_id    = self.load_and_compile_shader(GL_VERTEX_SHADER, "normalRender.vert")
		fragment_shader_id  = self.load_and_compile_shader(GL_FRAGMENT_SHADER, "normalRender.frag")
		glAttachShader(self.program, vertex_shader_id)
		glAttachShader(self.program, fragment_shader_id)
		glLinkProgram(self.program)
			
		message = glGetProgramInfoLog(self.program)
		if message:
			print("[Shader linking failed]")
			print(message)
		# free up the now-unnecessary shader binaries
		glDeleteShader(vertex_shader_id)
		glDeleteShader(fragment_shader_id)
		glUseProgram(0)
		self.genBuffers()
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
		glUniform1i(	self.texLoc, 0)

		glBindVertexArray(self.vaos)
		
		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
		glBindVertexArray(0)
		glBindTexture(GL_TEXTURE_2D, 0)
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
		
	def vec3toNp(vec3):
		return np.array(vec3.x,vec3.y,vec3.z, dtype='f')
	
	def genBuffers(self):
		# generate VAO, VBO
		self.vaos = glGenVertexArrays(1)
		self.vbos = glGenBuffers(1)
		
		float_size = sizeof(c_float)
		
		#    x, y, z,    r, g, b,     s, t
		self.vertices = np.array( [
			-1, 0, -1,  1, 0, 0,	 0, 0,
			-1, 0,  1,  0, 1, 0,     0, 1,
			 1, 0, -1,  0, 0, 1,	 1, 0,
			 1, 0,  1,  1, 1, 1, 	 1, 1,
		
		], dtype = 'f')
		
		glBindVertexArray(self.vaos)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbos)
		glBufferData(GL_ARRAY_BUFFER, float_size*(3+3+2)*4, self.vertices, GL_STREAM_DRAW)
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0, 3, GL_FLOAT, False, float_size*(3+3+2), c_void_p(0 * float_size) )
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(1, 3, GL_FLOAT, False, float_size*(3+3+2), c_void_p(3 * float_size) )
		glEnableVertexAttribArray(2)
		glVertexAttribPointer(2, 2, GL_FLOAT, False, float_size*(3+3+2), c_void_p(6 * float_size) )
		
		#glEnable(GL_CULL_FACE)
		
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
	