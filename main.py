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
from win32api import GetSystemMetrics

class Main(QGLWidget):
	def __init__(self, surface = 'sphere'):
		
		super(Main, self).__init__()
		self.setGeometry( 302,38, GetSystemMetrics(0) - 325 - 302, GetSystemMetrics(1) )
		self.fps_last_time = 0
		self.fps_frame_count = 0		
		self.times = []
		self.texture_program = None
		self.photon_birth_program = None
		self.photon_simulation_program = None
		self.param_program = None
		self.camera = Camera(Vector3(0,0,15), Vector3(0,0,0), Vector3(0,1,0))
		self.last_time = 0
		self.delta_time = 0
		self.fbo_created = False
		self.light_sources_modified = True
		self.texw, self.texh = 1024,1024
		self.framebuffer = None
		self.fbo_texture = None
		
		self.time = 0
		self.in_pause = False
		
		self.total_light_power = 0.0
		self.photon_birth_count = None #16#1024*2
		self.max_photons = 1024*1024
		self.free_photons = self.max_photons
		self.min_photon_energy = 0.03
								   # Radius_1	 height	 radius_2	 param4
		self.param_surface_params = [5.,		 5., 	1., 		0.]
										
		#								x	y		power	photoncount	from		to	wl		dummy
		self.light_sources = np.array( [0.25,	0.25,		1,		256,			0,		0,	400,	0,   
										0.75, 	0.5,		0.5, 	256, 			0, 		0, 	550, 	0], dtype = 'f')
		self.lightsource_num = 2
		self.light_size = len(self.light_sources)/self.lightsource_num
		#								r1	r2	h	k1	k2	dummies
		self.surface_params = np.array([3., 1., 5., 1., 1., 0, 0, 0 ],dtype = 'f')
		to_load = surface + '/f.txt'
		concat_files_to_shader("simulationOfPhotons_begin.compute", to_load, "simulationOfPhotons_end.compute")
		concat_files_to_shader("parametricSurface_begin.tes", to_load, "parametricSurface_end.tes")
		
	def initializeGL(self):
		pygame.init()
		print( "Running OpenGL %s.%s" % (glGetInteger(GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION)) )
		try:
			self.photon_birth_program		= create_program(compute_file = "birthOfPhotons.compute")
			self.photon_simulation_program	= create_program(compute_file = "simulationOfPhotons.compute")
			self.param_program				= create_program(vertex_file = "parametricSurface.vert", fragment_file = "parametricSurface.frag", tess_con_file = "parametricSurface.tcs", tess_eval_file = "parametricSurface.tes")
			self.texture_program			= create_program(vertex_file = "geom/renderToTexture.vert", fragment_file = "geom/renderToTexture.frag", geom_file = "geom/renderToTexture.geom")
		except Exception as error:
			print (error)
			QtCore.QCoreApplication.quit()
			sys.exit()

		self.vaos, self.vbos, self.lightSourceBuffer, self.emptyIndices, self.input_pos, self.output_pos, self.photonBuffer, self.atomic, self.surfaceParamsBuffer = genBuffers(self.light_sources, self.max_photons, self.light_size, self.lightsource_num, self.surface_params)
		self.fbo_created, self.framebuffer, self.fbo_texture = genFBO(self.fbo_created, self.framebuffer, self.fbo_texture, self.texw, self.texh)
		glEnable(GL_CULL_FACE)

	def paintGL(self):
		#update
		self.compute_time()
		self.measure_FPS()
		self.camera.update(self.delta_time)
		if self.light_sources_modified:
			self.modify_light_buffers()	
			
		#render
		if not self.in_pause:
			self.use_photon_birth_program()
			
			glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT | GL_ATOMIC_COUNTER_BARRIER_BIT)
			
			self.use_photon_simulation_program()
			
			glMemoryBarrier(GL_VERTEX_ATTRIB_ARRAY_BARRIER_BIT | GL_SHADER_STORAGE_BARRIER_BIT)
			
		#debug
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, self.atomic)
		atomicCountDebug = glGetBufferSubData(GL_ATOMIC_COUNTER_BUFFER,0,1*sizeof(c_int))
		self.free_photons = atomicCountDebug[3]*256*256*256+atomicCountDebug[2]*256*256 + atomicCountDebug[1]*256 +atomicCountDebug[0] - 1073741824
		#print "atomicCountDebug = ", asd	
		
		self.use_texture_program()
		
		#glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
		
		self.use_param_program()
		
		self.update()
		
	def use_photon_birth_program(self):
		glUseProgram(self.photon_birth_program)
		glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, self.atomic)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.photonBuffer)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.emptyIndices)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.lightSourceBuffer)
		glUniform1f(0, self.time)
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
		glUniform1f(1, self.time)
		glUniform1f(2, self.min_photon_energy)
		glUniform4fv(3, 1, self.param_surface_params)
		glDispatchCompute(self.max_photons, 1, 1)
		glFinish()
		glUseProgram(0)
		
	def use_texture_program(self):
		glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
		glViewport(0,0,self.texw,self.texh)
		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		glEnable(GL_BLEND)
		glBlendEquation(GL_FUNC_ADD)
		glBlendFunc(GL_ONE, GL_ONE)
		
		glUseProgram(self.texture_program)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.input_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.output_pos)
		glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.photonBuffer)
		glBindVertexArray(0)
		glDrawArrays(GL_POINTS, 0, self.max_photons)
		glBindVertexArray(0)
		self.input_pos, self.output_pos = self.output_pos, self.input_pos
		glUseProgram(0)
		
		glDisable(GL_BLEND)
		
	def use_param_program(self):
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		glEnable(GL_DEPTH_TEST)
		glViewport(0,0, self.size().width(), self.size().height())
		glClearColor(0.2, 0.3, 0.4, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
		glUseProgram(self.param_program)
		matWorld = Matrix4()
		matWorldIT = matWorld.inverse().transposed()
		mvp = self.camera.matViewProj * matWorld
		glUniformMatrix4fv(0, 1, GL_FALSE, c_matrix(matWorld))
		glUniformMatrix4fv(4, 1, GL_FALSE, c_matrix(matWorldIT))
		glUniformMatrix4fv(8, 1, GL_FALSE, c_matrix(mvp))
		glUniform3fv(12, 1, [self.camera.getEye().x,self.camera.getEye().y, self.camera.getEye().z])
		glUniform4fv(16, 1, self.param_surface_params)
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
				self.setWindowTitle( str(1000.0*float(self.fps_delta_time)/self.fps_frame_count) + " ms, " + str(self.fps_frame_count) + " FPS" + " free photons = " + str(self.free_photons))
				self.times.append( self.fps_frame_count )
			self.fps_frame_count = 0
			self.fps_last_time = time.time()
				
	def modify_light_buffers(self):
		c_photon_until_now = 0
		s = 8 #number of one lightsource's parameters
		for i in range(self.lightsource_num):
			self.light_sources[i*s+4] = c_photon_until_now
			c_photon_until_now += self.light_sources[i*s+3]
			self.light_sources[i*s+5] = c_photon_until_now - 1
			
		self.photon_birth_count = int(c_photon_until_now)	
		
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.lightSourceBuffer)
		glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, self.light_size * self.lightsource_num * sizeof(c_float),self.light_sources)
		self.light_sources_modified = False
			
	def resizeGL(self, w, h):
		print w, h
		print self.size().width(), self.size().height()
		self.camera.setProjMatrix(55.0, w/float(h), 0.001, 100.0)
		
	def closeEvent(self, event):
		print "end"
		self.close()
		#delete stuff
		
	def keyPressEvent(self, e):
		self.camera.keyboardDown(e)
		if e.key() == Qt.Key_Escape:
			self.close()
		if e.key() == Qt.Key_Plus:
			self.wavelength = min(self.wavelength + 1, 750)
		if e.key() == Qt.Key_Minus:
			self.wavelength = max(self.wavelength - 1, 390)
		if e.key() == Qt.Key_Space:
			self.in_pause = not self.in_pause

	def mousePressEvent(self, e):
		self.camera.click(e)
		
	def keyReleaseEvent(self,e):
		self.camera.keyboardUp(e)
			
	def mouseMoveEvent(self,e):
		self.camera.mouseMove(e, self.delta_time)
	
	def wheelEvent(self,e):
		self.camera.mouseWheel(e.angleDelta().y()/120)
	
	def compute_time(self):
		this_time = pygame.time.get_ticks()/1000.0
		self.delta_time = (this_time - self.last_time)
		self.last_time = this_time		
		if not self.in_pause:
			self.time += self.delta_time
			
	def set_max_photon(self, max_photons):
		self.max_photons = max_photons
	
	def set_min_photon_power(self, min_photon_energy):
		self.min_photon_energy = min_photon_energy
		
	def update_surface(self, params):
		r1, r2, h, k1, k2 = 0., 0., 0., 0., 0.
		for k in ['r1', 'r2', 'h', 'k1', 'k2']:
			if k in params.keys():
				exec("%s = %f" % (k,params[k]))
		self.surface_params = np.array([r1, r2, h, k1, k2, 0, 0, 0], dtype = 'f')
		glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.surfaceParamsBuffer)
		glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, 8*sizeof(c_float),self.surface_params)
		
'''if __name__ == '__main__':
	pygame.init()
	app = QtWidgets.QApplication(["PyQt OpenGL speed benchmark"])
	widget = Main()
	widget.show()
	app.exec_()
	print np.mean( widget.times )'''
	
	
'''app = QtWidgets.QApplication(["PyQt OpenGL speed benchmark"])
	screen = Select_Surface()
	screen.show()
	app.exec_()'''