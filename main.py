from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtOpenGL import *
import numpy as np
import time
from ctypes import sizeof, c_float, c_void_p, c_int
from math import *
from camera import *
import sys
sys.path.insert(0, 'C:/Users/Panni/thesis_in_Python/pyeuclid')
from euclid import *
import pygame.time
import pygame
from shaderProgram import create_program
from util import *

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
		self.camera = Camera(Vector3(10,10,10), Vector3(0,0,0), Vector3(0,1,0))
		self.last_time = 0
		self.delta_time = 0
		self.max_photons = 1024*512
		self.photon_birth_count = 1024
		self.fbo_created = False
		self.lightsource_num = 2
		self.total_light_power = 0.0
		self.light_sources_modified = True
		self.light_size = 8
		self.framebuffer = None
		self.fbo_texture = None
		
	def initializeGL(self):
		print( "Running OpenGL %s.%s" % (glGetInteger(GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION)) )		
		self.photon_birth_program		= create_program(compute_file = "birthOfPhotons.compute")
		self.photon_simulation_program	= create_program(compute_file = "simulationOfPhotons.compute")
		self.param_program				= create_program(vertex_file = "parametricSurface.vert", fragment_file = "parametricSurface.frag", tess_con_file = "parametricSurface.tcs", tess_eval_file = "parametricSurface.tes")
		self.texture_program			= create_program(vertex_file = "renderToTexture.vert", fragment_file = "renderToTexture.frag")

		#glPointSize(5.0)
		#								x y  power photoncount from, to  dummies
		self.light_sources = np.array([0, 0, 0.5,    0,          0,    0,  0, 0,   0.5, 0.5, 0.5, 0, 0, 0, 0, 0], dtype = 'f')
		self.vaos, self.vbos, self.lightSourceBuffer, self.emptyIndices, self.input_pos, self.output_pos, self.photonBuffer, self.atomic = genBuffers(self.light_sources, self.max_photons, self.light_size, self.lightsource_num)
		glEnable(GL_CULL_FACE)

	#render
	def paintGL(self):
		self.measure_FPS()
		
		#update
		this_time = pygame.time.get_ticks()/1000.0
		self.delta_time = (this_time - self.last_time)
		self.last_time = this_time
		self.camera.update(self.delta_time)

		if self.light_sources_modified:
			self.modify_light_buffers()
		
		self.use_photon_birth_program()
		
		glFinish()
		glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT | GL_ATOMIC_COUNTER_BARRIER_BIT)
		
		self.use_photon_simulation_program()
		
		glMemoryBarrier(GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT)
		glFinish()
		
		#debug
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, self.atomic)
		atomicCountDebug = glGetBufferSubData(GL_ATOMIC_COUNTER_BUFFER,0,1*sizeof(c_int))
		asd = atomicCountDebug[3]*256*256*256+atomicCountDebug[2]*256*256 + atomicCountDebug[1]*256 +atomicCountDebug[0] - 1073741824
		#print "atomicCountDebug = ", asd
		
		#render
		glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
		glViewport(0,0,1024,1024)
		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT)		

		self.use_texture_program()
		
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		glViewport(0,0, self.size().width(), self.size().height())
		glClearColor(0.2, 0.3, 0.4, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		
		self.use_param_program()
		
		self.update()
		
	def use_photon_birth_program(self):
		glUseProgram(self.photon_birth_program)
		glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, self.atomic)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.photonBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.emptyIndices)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.lightSourceBuffer)
		glUniform1f(0, pygame.time.get_ticks()/1000.0)
		glUniform1i(1, self.photon_birth_count)
		glUniform1i(2, self.lightsource_num)
		glUniform1f(3, self.total_light_power)
		glDispatchCompute(self.photon_birth_count,1,1)
		glFinish()
		glUseProgram(0)
		
	def use_photon_simulation_program(self):
		glUseProgram(self.photon_simulation_program)
		glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, self.atomic)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.photonBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.emptyIndices)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.output_pos)
		glUniform1f(0, self.delta_time)
		glUniform1f(1, pygame.time.get_ticks()/1000.0)
		glDispatchCompute(self.max_photons, 1, 1)
		glFinish()
		glUseProgram(0)
		
	def use_texture_program(self):
		glUseProgram(self.texture_program)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.output_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.photonBuffer)
		glBindVertexArray(0)
		glDrawArrays(GL_LINES, 0, self.max_photons*2)
		glBindVertexArray(0)
		self.input_pos, self.output_pos = self.output_pos, self.input_pos
		glUseProgram(0)
		
	def use_param_program(self):
		glUseProgram(self.param_program)
		matWorld = Matrix4()
		matWorldIT = matWorld.inverse().transposed()
		mvp = self.camera.matViewProj * matWorld
		glUniformMatrix4fv(0, 1, GL_FALSE, c_matrix(matWorld))
		glUniformMatrix4fv(4, 1, GL_FALSE, c_matrix(matWorldIT))
		glUniformMatrix4fv(8, 1, GL_FALSE, c_matrix(mvp))
		glUniform3fv(12, 1, [self.camera.getEye().x,self.camera.getEye().y, self.camera.getEye().z])
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
		glBindVertexArray(self.vaos)
		glPatchParameteri(GL_PATCH_VERTICES, 1);
		glDrawArrays(GL_PATCHES, 0, 1)
		glBindVertexArray(0)
		glBindTexture(GL_TEXTURE_2D, 0)
		glUseProgram(0)
		
	def measure_FPS(self):
		self.fps_frame_count += 1
		self.fps_delta_time = abs( time.time() - self.fps_last_time )
		if self.fps_delta_time >= 1:
			if self.fps_frame_count:
				self.setWindowTitle( str(1000.0*float(self.fps_delta_time)/self.fps_frame_count) + " ms, " + str(self.fps_frame_count) + " FPS"  )
				self.times.append( self.fps_frame_count )
			self.fps_frame_count = 0
			self.fps_last_time = time.time()
				
	def modify_light_buffers(self):
			#melyik fenyforras hany fotont indit, kezdo foton index, utolso foton index:
			self.total_light_power = 0.0
			c_photon_until_now = 0
			for i in range(self.lightsource_num):
				self.total_light_power += self.light_sources[i*self.light_size + 2]
			for i in range(self.lightsource_num):
				#					photoncount
				self.light_sources[i*self.light_size + 3] = floor(self.light_sources[i*self.light_size + 2] / float(self.total_light_power) * self.photon_birth_count)
				self.light_sources[i*self.light_size + 4] = c_photon_until_now
				c_photon_until_now += self.light_sources[i*self.light_size + 3]
				self.light_sources[i*self.light_size + 5] = c_photon_until_now - 1
				if i == self.lightsource_num - 1: #for the very last photon
					self.light_sources[i*self.light_size + 5] = self.photon_birth_count - 1
				print 'photoncount', self.light_sources[i*self.light_size + 3]
				print 'start photon', self.light_sources[i*self.light_size + 4]
				print 'end photon', self.light_sources[i*self.light_size + 5]
				
			glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.lightSourceBuffer)
			glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, self.light_size * self.lightsource_num * sizeof(c_float),self.light_sources)
			self.light_sources_modified = False
			
	def resizeGL(self, w, h):
		#glViewport(0, 0, w-1, h-1)
		self.fbo_created, self.framebuffer, self.fbo_texture = genFBO(self.fbo_created, self.framebuffer, self.fbo_texture)
		print w, h
		print self.size().width(), self.size().height()
		self.camera.setProjMatrix(50.0, w/float(h), 0.001, 100.0)
		
	def closeEvent(self, event):
		print "end"
		#delete stuff
		
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
		
if __name__ == '__main__':
	pygame.init()
	app = QtWidgets.QApplication(["PyQt OpenGL speed benchmark"])
	widget = Main()
	widget.show()
	app.exec_()
	print np.mean( widget.times )
	