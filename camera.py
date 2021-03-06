from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtOpenGL import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, 
    QVBoxLayout, QApplication)
import numpy as np
from numpy import linalg as LA
import time
import math
sys.path.insert(0, 'C:/Users/Panni/thesis_in_Python/pyeuclid')
from euclid import *

class Camera():
	def __init__(self, eye = Vector3(0,0,15), at = Vector3(0,0,0), up = Vector3(0,1,0)):
		self.lookAt(eye, at, up)
		self.viewMatrix  = Matrix4()
		self.setProjMatrix(50.0, 640/480.0, 0.001, 1000.0)
		self.setViewMatrix(eye);
		self.goFw = 0.0
		self.goRight = 0.0
		self.old_x = 0
		self.old_y = 0
		self.speed = 2.0
		self.eye = eye
			
	def update(self, deltatime):
		s = Vector3(math.cos(self.v)*math.cos(self.u),
					math.cos(self.v)*math.sin(self.u),
					math.sin(self.v))
		m = Matrix4()
		m[0:16] = (self.x.x, self.x.y, self.x.z,0,
					self.y.x, self.y.y, self.y.z,0,
					self.up.x, self.up.y, self.up.z,0,
					0,0,0,1)
		toeye = m * s
		forward = -toeye
		right = forward.cross(self.up).normalize()
		self.at  += forward*deltatime*self.speed*self.goFw + right*deltatime*self.speed*self.goRight
		eye = self.at + (toeye * self.dist)
		self.setViewMatrix(eye);
	
	def setSpeed(self, val):
		self.speed = val
		
	def resize(self, w, h):
		self.projMatrix = perspective(45.0, w/h, 0.01, 1000.0)
		self.matViewProj = self.projMatrix * self.viewMatrix
	
	def keyboardDown(self, e):
		if e.key() == Qt.Key_Left or e.key() == Qt.Key_A :
			self.goRight = -1
		if e.key() == Qt.Key_Right or e.key() == Qt.Key_D:
			self.goRight = 1 
		if e.key() == Qt.Key_Up or e.key() == Qt.Key_W:
			self.goFw = 1
		if e.key() == Qt.Key_Down or e.key() == Qt.Key_S:
			self.goFw = -1
		if e.key() == Qt.Key_C:
			self.toCenter()
			
	def keyboardUp(self, e):
		if e.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_A, Qt.Key_D]:
			self.goRight = 0
		if e.key() in [Qt.Key_Up,  Qt.Key_Down, Qt.Key_W, Qt.Key_S]:
			self.goFw = 0
			
	def mouseMove(self, e, deltatime):
		self.u -= (e.x() - self.old_x)*deltatime*0.5
		self.v += (e.y() - self.old_y)*deltatime*0.5
		epsilon = 0.001
		self.v = max(-math.pi/2 + epsilon , min(self.v, math.pi/2-epsilon))
		self.old_x = e.x()
		self.old_y = e.y()
	
	def mouseWheel(self, delta):
		self.dist *= 1-0.05*delta
	
	def click(self, e):
		if e.button() == Qt.LeftButton:
			self.old_x = e.x()
			self.old_y = e.y()

	def lookAt(self, eye, at, up):
		self.up = up
		self.x = up.cross(Vector3(1,0,0)).normalize()
		self.y = up.cross(self.x).normalize()
		m = Matrix4()
		m[0:16] = (self.x.x, self.y.x, self.up.x, 0, self.x.y, self.y.y, self.up.y, 0, self.x.z, self.y.z, self.up.z, 0, 0,0,0,1)
		s = m * ((eye - at).normalize())
		self.v = math.asin(s.z)
		self.u = math.atan2(s.y, s.x)
		self.at = at
		self.eye = eye
		self.dist = abs(at-eye);
		
	def setProjMatrix(self, angle, aspect, zn, zf):
		self.projMatrix = Matrix4.new_perspective(math.pi*angle/180.0, aspect, zn, zf)
		self.matViewProj = self.projMatrix * self.viewMatrix
	
	def setViewMatrix(self, eye):
		self.viewMatrix = Matrix4.new_look_at(eye, self.at, self.up)
		self.matViewProj = self.projMatrix * self.viewMatrix
		self.eye = eye

	def toCenter(self):
		self.lookAt(Vector3(0,0,15), Vector3(), Vector3(0,1,0))
		self.setViewMatrix(Vector3(0,0,15))
		
	def getEye(self):
		return self.eye
		