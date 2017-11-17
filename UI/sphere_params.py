# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sphere_params.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Sphere_Parameters(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setupUi()
		self.setGeometry(1, 410, 300, 130)
		
	def setupUi(self):
		self.setObjectName("Form")
		self.resize(300, 130)
		self.gridLayoutWidget = QtWidgets.QWidget(self)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 10, 181, 91))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
		self.doubleSpinBox_r = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.doubleSpinBox_r.setDecimals(1)
		self.doubleSpinBox_r.setMinimum(0.1)
		self.doubleSpinBox_r.setMaximum(10.0)
		self.doubleSpinBox_r.setSingleStep(0.1)
		self.doubleSpinBox_r.setProperty("value", 1.0)
		self.doubleSpinBox_r.setObjectName("doubleSpinBox_r")
		self.gridLayout.addWidget(self.doubleSpinBox_r, 2, 1, 1, 1)
		self.pushButton_update = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton_update.setObjectName("pushButton_update")
		self.gridLayout.addWidget(self.pushButton_update, 3, 0, 1, 2)
		self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
	
		self.retranslateUi()
	
	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "Sphere parameters"))
		self.label_3.setText(_translate("Form", "Radius"))
		self.pushButton_update.setText(_translate("Form", "Update"))
		self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Sphere</span></p></body></html>"))
	
	def get_surface_params(self):
		params = {'r1': self.doubleSpinBox_r.value()}
		return params
	
	def closeEvent(self, event):
		self.close()
