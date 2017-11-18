# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'light_source_settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from add_new_ls import *
from win32api import GetSystemMetrics
import numpy as np

class Light_Source_Settings(QtWidgets.QWidget):
	def __init__(self, lights = np.array([], dtype = 'f'), n = 0): #lights : np array = light_sources
		QtWidgets.QWidget.__init__(self)		
		self.setupUi(lights, n)
		self.setGeometry(GetSystemMetrics(0) - 325, 38, 325, GetSystemMetrics(1))
		self.new_ls = None
		self.pushButton_add_new.clicked.connect(self.add_new)
		
	def setupUi(self, lights, n):
		self.setObjectName("Form")
		self.resize(325, 855)
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
		
		self.generate_light_sources(n, lights)
		
		'''self.widget = QtWidgets.QWidget(self)
		self.widget.setGeometry(QtCore.QRect(10, 350, 299, 148))
		self.widget.setObjectName("widget")
		self.gridLayout_0 = QtWidgets.QGridLayout(self.widget)
		self.gridLayout_0.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_0.setObjectName("gridLayout_0")
		self.doubleSpinBox_ypos_0 = QtWidgets.QDoubleSpinBox(self.widget)
		self.doubleSpinBox_ypos_0.setMaximum(1.0)
		self.doubleSpinBox_ypos_0.setSingleStep(0.1)
		self.doubleSpinBox_ypos_0.setProperty("value", 0.5)
		self.doubleSpinBox_ypos_0.setObjectName("doubleSpinBox_ypos_0")
		self.gridLayout_0.addWidget(self.doubleSpinBox_ypos_0, 1, 4, 1, 1)
		self.label_7 = QtWidgets.QLabel(self.widget)
		self.label_7.setObjectName("label_7")
		self.gridLayout_0.addWidget(self.label_7, 1, 3, 1, 1)
		self.label_8 = QtWidgets.QLabel(self.widget)
		self.label_8.setMaximumSize(QtCore.QSize(16777215, 16770000))
		self.label_8.setObjectName("label_8")
		self.gridLayout_0.addWidget(self.label_8, 0, 0, 1, 5)
		self.doubleSpinBox_xpos_0 = QtWidgets.QDoubleSpinBox(self.widget)
		self.doubleSpinBox_xpos_0.setMaximum(1.0)
		self.doubleSpinBox_xpos_0.setSingleStep(0.1)
		self.doubleSpinBox_xpos_0.setProperty("value", 0.5)
		self.doubleSpinBox_xpos_0.setObjectName("doubleSpinBox_xpos_0")
		self.gridLayout_0.addWidget(self.doubleSpinBox_xpos_0, 1, 2, 1, 1)
		self.doubleSpinBox_pow_0 = QtWidgets.QDoubleSpinBox(self.widget)
		self.doubleSpinBox_pow_0.setMaximum(1.0)
		self.doubleSpinBox_pow_0.setSingleStep(0.1)
		self.doubleSpinBox_pow_0.setProperty("value", 1.0)
		self.doubleSpinBox_pow_0.setObjectName("doubleSpinBox_pow_0")
		self.gridLayout_0.addWidget(self.doubleSpinBox_pow_0, 2, 4, 1, 1)
		self.spinBox_ppf_0 = QtWidgets.QSpinBox(self.widget)
		self.spinBox_ppf_0.setMaximum(2048)
		self.spinBox_ppf_0.setProperty("value", 512)
		self.spinBox_ppf_0.setObjectName("spinBox_ppf_0")
		self.gridLayout_0.addWidget(self.spinBox_ppf_0, 2, 2, 1, 1)
		self.label_9 = QtWidgets.QLabel(self.widget)
		self.label_9.setObjectName("label_9")
		self.gridLayout_0.addWidget(self.label_9, 2, 3, 1, 1)
		self.label_10 = QtWidgets.QLabel(self.widget)
		self.label_10.setObjectName("label_10")
		self.gridLayout_0.addWidget(self.label_10, 1, 0, 1, 2)
		self.label_11 = QtWidgets.QLabel(self.widget)
		self.label_11.setObjectName("label_11")
		self.gridLayout_0.addWidget(self.label_11, 2, 0, 1, 2)
		self.label_17 = QtWidgets.QLabel(self.widget)
		self.label_17.setObjectName("label_17")
		self.gridLayout_0.addWidget(self.label_17, 3, 0, 1, 1)
		self.horizontalSlider = QtWidgets.QSlider(self.widget)
		self.horizontalSlider.setMinimum(380)
		self.horizontalSlider.setMaximum(780)
		self.horizontalSlider.setSingleStep(10)
		self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
		self.horizontalSlider.setObjectName("horizontalSlider")
		self.gridLayout_0.addWidget(self.horizontalSlider, 3, 2, 1, 3)
		self.label_18 = QtWidgets.QLabel(self.widget)
		self.label_18.setObjectName("label_18")
		self.gridLayout_0.addWidget(self.label_18, 3, 1, 1, 1)
		self.pushButton_mod_6 = QtWidgets.QPushButton(self.widget)
		self.pushButton_mod_6.setObjectName("pushButton_mod_6")
		self.gridLayout_0.addWidget(self.pushButton_mod_6, 4, 3, 1, 2)
		self.pushButton_mod_7 = QtWidgets.QPushButton(self.widget)
		self.pushButton_mod_7.setObjectName("pushButton_mod_7")
		self.gridLayout_0.addWidget(self.pushButton_mod_7, 4, 0, 1, 3)
		
		self.widget1 = QtWidgets.QWidget(self)
		self.widget1.setGeometry(QtCore.QRect(10, 500, 299, 148))
		self.widget1.setObjectName("widget1")
		self.gridLayout_1 = QtWidgets.QGridLayout(self.widget1)
		self.gridLayout_1.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_1.setObjectName("gridLayout_1")
		self.doubleSpinBox_ypos_3 = QtWidgets.QDoubleSpinBox(self.widget1)
		self.doubleSpinBox_ypos_3.setMaximum(1.0)
		self.doubleSpinBox_ypos_3.setSingleStep(0.1)
		self.doubleSpinBox_ypos_3.setProperty("value", 0.5)
		self.doubleSpinBox_ypos_3.setObjectName("doubleSpinBox_ypos_3")
		self.gridLayout_1.addWidget(self.doubleSpinBox_ypos_3, 1, 4, 1, 1)
		self.label_12 = QtWidgets.QLabel(self.widget1)
		self.label_12.setObjectName("label_12")
		self.gridLayout_1.addWidget(self.label_12, 1, 3, 1, 1)
		self.label_13 = QtWidgets.QLabel(self.widget1)
		self.label_13.setMaximumSize(QtCore.QSize(16777215, 16770000))
		self.label_13.setObjectName("label_13")
		self.gridLayout_1.addWidget(self.label_13, 0, 0, 1, 5)
		self.doubleSpinBox_xpos_3 = QtWidgets.QDoubleSpinBox(self.widget1)
		self.doubleSpinBox_xpos_3.setMaximum(1.0)
		self.doubleSpinBox_xpos_3.setSingleStep(0.1)
		self.doubleSpinBox_xpos_3.setProperty("value", 0.75)
		self.doubleSpinBox_xpos_3.setObjectName("doubleSpinBox_xpos_3")
		self.gridLayout_1.addWidget(self.doubleSpinBox_xpos_3, 1, 2, 1, 1)
		self.doubleSpinBox_pow_3 = QtWidgets.QDoubleSpinBox(self.widget1)
		self.doubleSpinBox_pow_3.setMaximum(1.0)
		self.doubleSpinBox_pow_3.setSingleStep(0.1)
		self.doubleSpinBox_pow_3.setProperty("value", 1.0)
		self.doubleSpinBox_pow_3.setObjectName("doubleSpinBox_pow_3")
		self.gridLayout_1.addWidget(self.doubleSpinBox_pow_3, 2, 4, 1, 1)
		self.spinBox_ppf_3 = QtWidgets.QSpinBox(self.widget1)
		self.spinBox_ppf_3.setMaximum(2048)
		self.spinBox_ppf_3.setProperty("value", 512)
		self.spinBox_ppf_3.setObjectName("spinBox_ppf_3")
		self.gridLayout_1.addWidget(self.spinBox_ppf_3, 2, 2, 1, 1)
		self.label_14 = QtWidgets.QLabel(self.widget1)
		self.label_14.setObjectName("label_14")
		self.gridLayout_1.addWidget(self.label_14, 2, 3, 1, 1)
		self.label_15 = QtWidgets.QLabel(self.widget1)
		self.label_15.setObjectName("label_15")
		self.gridLayout_1.addWidget(self.label_15, 1, 0, 1, 2)
		self.label_16 = QtWidgets.QLabel(self.widget1)
		self.label_16.setObjectName("label_16")
		self.gridLayout_1.addWidget(self.label_16, 2, 0, 1, 2)
		self.label_19 = QtWidgets.QLabel(self.widget1)
		self.label_19.setObjectName("label_19")
		self.gridLayout_1.addWidget(self.label_19, 3, 0, 1, 1)
		self.horizontalSlider_2 = QtWidgets.QSlider(self.widget1)
		self.horizontalSlider_2.setMinimum(380)
		self.horizontalSlider_2.setMaximum(780)
		self.horizontalSlider_2.setSingleStep(10)
		self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
		self.horizontalSlider_2.setObjectName("horizontalSlider_2")
		self.gridLayout_1.addWidget(self.horizontalSlider_2, 3, 2, 1, 3)
		self.label_20 = QtWidgets.QLabel(self.widget1)
		self.label_20.setObjectName("label_20")
		self.gridLayout_1.addWidget(self.label_20, 3, 1, 1, 1)
		self.pushButton_mod_8 = QtWidgets.QPushButton(self.widget1)
		self.pushButton_mod_8.setObjectName("pushButton_mod_8")
		self.gridLayout_1.addWidget(self.pushButton_mod_8, 4, 3, 1, 2)
		self.pushButton_mod_9 = QtWidgets.QPushButton(self.widget1)
		self.pushButton_mod_9.setObjectName("pushButton_mod_9")
		self.gridLayout_1.addWidget(self.pushButton_mod_9, 4, 0, 1, 3)'''
	
		self.retranslateUi(n)
	
	def retranslateUi(self, n):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "Light Source Settings"))
		self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Light Sources</span></p></body></html>"))
		self.pushButton_add_new.setText(_translate("Form", "Add new"))
		
		for i in range(n):
			self.label_y[i].setText(_translate("Form", "  y  ")) #label_y_0
			self.label_ls[i].setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Light source #" + str(i+1) + "</span></p></body></html>")) #label_ls_n
			self.label_pow[i].setText(_translate("Form", "Power")) #label_pow_0
			self.label_x[i].setText(_translate("Form", "  x  ")) #label_x_0
			self.label_ppf[i].setText(_translate("Form", "Photons per frame")) #label_ppf_0
			self.label_wl[i].setText(_translate("Form", "Wavelength")) #label_wl_0
			self.label_num[i].setText(_translate("Form", "num")) #label_num_0
			self.pushButton_delete[i].setText(_translate("Form", "Delete")) #pushButton_delete_0
			self.pushButton_modify[i].setText(_translate("Form", "Modify"))
		'''self.label_12.setText(_translate("Form", "  y  "))
		self.label_13.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Light source #n</span></p></body></html>"))
		self.label_14.setText(_translate("Form", "Power"))
		self.label_15.setText(_translate("Form", "  x  "))
		self.label_16.setText(_translate("Form", "Photons per frame"))
		self.label_19.setText(_translate("Form", "Wavelength"))
		self.label_20.setText(_translate("Form", "num"))
		self.pushButton_mod_8.setText(_translate("Form", "Delete"))
		self.pushButton_mod_9.setText(_translate("Form", "Modify"))'''
	
	
	def closeEvent(self, event):
		if self.new_ls is not None:
			self.new_ls.closeEvent(event)
		self.close()
		
	def add_new(self):
		self.new_ls = Add_New_LS()
		self.new_ls.show()
		
	def generate_light_sources(self, n, lights):
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
			print len(self.widgets), i
			self.widgets[i] = QtWidgets.QWidget(self)
			self.widgets[i].setGeometry(QtCore.QRect(10, 350 + i * 150, 299, 148))
			self.widgets[i].setObjectName("widget_" + str(i))
			self.gridLayouts[i] = QtWidgets.QGridLayout(self.widgets[i])
			self.gridLayouts[i].setContentsMargins(0, 0, 0, 0)
			self.gridLayouts[i].setObjectName("gridLayout_" + str(i))
			self.doubleSpinBox_ypos[i] = QtWidgets.QDoubleSpinBox(self.widgets[i])
			self.doubleSpinBox_ypos[i].setMaximum(1.0)
			self.doubleSpinBox_ypos[i].setSingleStep(0.1)
			self.doubleSpinBox_ypos[i].setProperty("value", lights[8*i+1])
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
			self.doubleSpinBox_xpos[i].setProperty("value", lights[8*i])
			self.doubleSpinBox_xpos[i].setObjectName("doubleSpinBox_xpos_" + str(i))
			self.gridLayouts[i].addWidget(self.doubleSpinBox_xpos[i], 1, 2, 1, 1)
			self.doubleSpinBox_pow[i] = QtWidgets.QDoubleSpinBox(self.widgets[i])
			self.doubleSpinBox_pow[i].setMaximum(1.0)
			self.doubleSpinBox_pow[i].setSingleStep(0.1)
			self.doubleSpinBox_pow[i].setProperty("value", lights[8*i+2])
			self.doubleSpinBox_pow[i].setObjectName("doubleSpinBox_pow_"+str(i))
			self.gridLayouts[i].addWidget(self.doubleSpinBox_pow[i], 2, 4, 1, 1)
			self.spinBox_ppf[i] = QtWidgets.QSpinBox(self.widgets[i])
			self.spinBox_ppf[i].setMaximum(2048)
			self.spinBox_ppf[i].setProperty("value", lights[8*i+3])
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
			self.horizontalSlider[i].setValue(lights[8*i+6])
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