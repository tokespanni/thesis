# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'light_source_settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from win32api import GetSystemMetrics
import numpy as np
sys.path.insert(0, 'C:/Users/Panni/thesis_in_Python/thesis')
from util import wavelength_to_rgb

class Light_Source_Settings(QtWidgets.QWidget):
	def __init__(self, lights, n):
		QtWidgets.QWidget.__init__(self)	
		self.lights = lights
		self.n = n
		print self.lights
		print self.n
		self.setupUi()
		self.setGeometry(GetSystemMetrics(0) - 325, 38, 325, GetSystemMetrics(1) - 25)
		
	def setupUi(self):
		self.setObjectName("Form")
		self.resize(325, GetSystemMetrics(1))
		self.gridLayoutWidget = QtWidgets.QWidget(self)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 301, 331))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
		self.pushButton_add_new = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton_add_new.setObjectName("pushButton_add_new")
		self.gridLayout.addWidget(self.pushButton_add_new, 2, 0, 1, 1)
		self.minimap = QtWidgets.QGraphicsView(self.gridLayoutWidget)
		self.minimap.setObjectName("minimap")
		self.gridLayout.addWidget(self.minimap, 1, 0, 1, 1)
		
		self.setMinimap()
		
		self.generate_light_sources()
	
		self.retranslateUi()
	
	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "Light Source Settings"))
		self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Light Sources</span></p></body></html>"))
		self.pushButton_add_new.setText(_translate("Form", "Add new"))
		
		for i in range(self.n):
			self.label_y[i].setText(_translate("Form", "  y  ")) #label_y_0
			self.label_ls[i].setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Light source #" + str(i+1) + "</span></p></body></html>")) #label_ls_n
			self.label_pow[i].setText(_translate("Form", "Power")) #label_pow_0
			self.label_x[i].setText(_translate("Form", "  x  ")) #label_x_0
			self.label_ppf[i].setText(_translate("Form", "Photons per frame")) #label_ppf_0
			self.label_wl[i].setText(_translate("Form", "Wavelength")) #label_wl_0
			self.label_num[i].setText(_translate("Form", "num")) #label_num_0
			self.pushButton_delete[i].setText(_translate("Form", "Delete")) #pushButton_delete_0
			self.pushButton_modify[i].setText(_translate("Form", "Modify"))
	
	def get_ls_params(self, i):
		return self.doubleSpinBox_xpos[i].value(), self.doubleSpinBox_ypos[i].value(), self.doubleSpinBox_pow[i].value(), self.spinBox_ppf[i].value(), self.horizontalSlider[i].value()
		
	def closeEvent(self, event):
		self.close()
		
	def update(self):
		self.generate_light_sources()
		self.setMinimap()
				
	def generate_light_sources(self):
		n = self.n
		self.widgets = [QtWidgets.QWidget(self)]*n
		self.gridLayouts = [QtWidgets.QWidget(self)]*n
		self.doubleSpinBox_ypos = [QtWidgets.QWidget(self)]*n
		self.label_x = [QtWidgets.QWidget(self)]*n
		self.doubleSpinBox_xpos = [QtWidgets.QWidget(self)]*n
		self.label_y = [QtWidgets.QWidget(self)]*n
		self.label_pow = [QtWidgets.QWidget(self)]*n
		self.doubleSpinBox_pow = [QtWidgets.QWidget(self)]*n
		self.label_ppf = [QtWidgets.QWidget(self)]*n
		self.spinBox_ppf = [QtWidgets.QWidget(self)]*n
		self.label_wl = [QtWidgets.QWidget(self)]*n
		self.horizontalSlider = [QtWidgets.QWidget(self)]*n
		self.label_num = [QtWidgets.QWidget(self)]*n
		self.pushButton_delete = [QtWidgets.QWidget(self)]*n
		self.pushButton_modify = [QtWidgets.QWidget(self)]*n
		self.label_ls = [QtWidgets.QWidget(self)]*n
		#								x	y		power	photoncount			from	to	wl		sn
		for i in range(n):
			self.widgets[i] = QtWidgets.QWidget(self)
			self.widgets[i].setGeometry(QtCore.QRect(10, 350 + i * 150, 299, 148))
			self.widgets[i].setObjectName("widget_" + str(i))
			self.gridLayouts[i] = QtWidgets.QGridLayout(self.widgets[i])
			self.gridLayouts[i].setContentsMargins(0, 0, 0, 0)
			self.gridLayouts[i].setObjectName("gridLayout_" + str(i))
			self.doubleSpinBox_ypos[i] = QtWidgets.QDoubleSpinBox(self.widgets[i])
			self.doubleSpinBox_ypos[i].setMaximum(1.0)
			self.doubleSpinBox_ypos[i].setSingleStep(0.1)
			self.doubleSpinBox_ypos[i].setProperty("value", float(self.lights[8*i+1]))
			self.doubleSpinBox_ypos[i].setObjectName("doubleSpinBox_ypos_" + str(i))
			self.gridLayouts[i].addWidget(self.doubleSpinBox_ypos[i], 1, 4, 1, 1)
			self.label_y[i] = QtWidgets.QLabel(self.widgets[i])
			self.label_y[i].setObjectName("label_y_" + str(i))
			self.gridLayouts[i].addWidget(self.label_y[i], 1, 3, 1, 1)
			self.label_ls[i] = QtWidgets.QLabel(self.widgets[i])
			self.label_ls[i].setMaximumSize(QtCore.QSize(16777215, 16770000))
			self.label_ls[i].setObjectName("label_ls" + str(i))
			self.gridLayouts[i].addWidget(self.label_ls[i], 0, 0, 1, 5)
			self.doubleSpinBox_xpos[i] = QtWidgets.QDoubleSpinBox(self.widgets[i])
			self.doubleSpinBox_xpos[i].setMaximum(1.0)
			self.doubleSpinBox_xpos[i].setSingleStep(0.1)
			self.doubleSpinBox_xpos[i].setProperty("value", float(self.lights[8*i]))
			self.doubleSpinBox_xpos[i].setObjectName("doubleSpinBox_xpos_" + str(i))
			self.gridLayouts[i].addWidget(self.doubleSpinBox_xpos[i], 1, 2, 1, 1)
			self.doubleSpinBox_pow[i] = QtWidgets.QDoubleSpinBox(self.widgets[i])
			self.doubleSpinBox_pow[i].setMaximum(1.0)
			self.doubleSpinBox_pow[i].setSingleStep(0.1)
			self.doubleSpinBox_pow[i].setProperty("value", float(self.lights[8*i+2]))
			self.doubleSpinBox_pow[i].setObjectName("doubleSpinBox_pow_"+str(i))
			self.gridLayouts[i].addWidget(self.doubleSpinBox_pow[i], 2, 4, 1, 1)
			self.spinBox_ppf[i] = QtWidgets.QSpinBox(self.widgets[i])
			self.spinBox_ppf[i].setMaximum(2048)
			self.spinBox_ppf[i].setProperty("value", float(self.lights[8*i+3]))
			self.spinBox_ppf[i].setObjectName("spinBox_ppf_"+str(i))
			self.gridLayouts[i].addWidget(self.spinBox_ppf[i], 2, 2, 1, 1)
			self.label_pow[i] = QtWidgets.QLabel(self.widgets[i])
			self.label_pow[i].setObjectName("label_pow_"+str(i))
			self.gridLayouts[i].addWidget(self.label_pow[i], 2, 3, 1, 1)
			self.label_x[i] = QtWidgets.QLabel(self.widgets[i])
			self.label_x[i].setObjectName("label_x_"+str(i))
			self.gridLayouts[i].addWidget(self.label_x[i], 1, 0, 1, 2)
			self.label_ppf[i] = QtWidgets.QLabel(self.widgets[i])
			self.label_ppf[i].setObjectName("label_ppf_"+str(i))
			self.gridLayouts[i].addWidget(self.label_ppf[i], 2, 0, 1, 2)
			self.label_wl[i] = QtWidgets.QLabel(self.widgets[i])
			self.label_wl[i].setObjectName("label_wl_"+str(i))
			self.gridLayouts[i].addWidget(self.label_wl[i], 3, 0, 1, 1)
			self.horizontalSlider[i] = QtWidgets.QSlider(self.widgets[i])
			self.horizontalSlider[i].setMinimum(380)
			self.horizontalSlider[i].setMaximum(780)
			self.horizontalSlider[i].setSingleStep(10)
			self.horizontalSlider[i].setValue(float(self.lights[8*i+6]))
			self.horizontalSlider[i].setOrientation(QtCore.Qt.Horizontal)
			self.horizontalSlider[i].setObjectName("horizontalSlider_"+str(i))
			self.gridLayouts[i].addWidget(self.horizontalSlider[i], 3, 2, 1, 3)
			self.label_num[i] = QtWidgets.QLabel(self.widgets[i])
			self.label_num[i].setObjectName("label_num_"+str(i))
			self.gridLayouts[i].addWidget(self.label_num[i], 3, 1, 1, 1)
			self.pushButton_delete[i] = QtWidgets.QPushButton(self.widgets[i])
			self.pushButton_delete[i].setObjectName("pushButton_delete_"+str(i))
			self.gridLayouts[i].addWidget(self.pushButton_delete[i], 4, 3, 1, 2)
			self.pushButton_modify[i] = QtWidgets.QPushButton(self.widgets[i])
			self.pushButton_modify[i].setObjectName("pushButton_modify_"+str(i))
			self.gridLayouts[i].addWidget(self.pushButton_modify[i], 4, 0, 1, 3)
			
	def setMinimap(self):
		self.minimap.scene = QtWidgets.QGraphicsScene(self)
		for i in range(self.n):
			rgb = wavelength_to_rgb(self.lights[8*i+6])
			self.minimap.scene.addEllipse(self.lights[8*i]*300, -self.lights[8*i+1]*300, 10, 10, QtGui.QPen(), QtGui.QBrush(QtGui.QColor(rgb[0], rgb[1], rgb[2])))
		
		self.minimap.setScene(self.minimap.scene)
		self.minimap.scene.setBackgroundBrush(QtCore.Qt.black)
		#print self.minimap.scene.sceneRect()
