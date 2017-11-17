# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proxy_circle_params.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Proxy_Circle_Parameters(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setupUi()
		self.setGeometry(1, 410, 300, 166)
		
	def setupUi(self):
		self.setObjectName("Form")
		self.resize(300, 166)
		self.gridLayoutWidget = QtWidgets.QWidget(self)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 10, 181, 148))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_4.setObjectName("label_4")
		self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
		self.doubleSpinBox_h = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.doubleSpinBox_h.setDecimals(1)
		self.doubleSpinBox_h.setMinimum(0.1)
		self.doubleSpinBox_h.setMaximum(10.0)
		self.doubleSpinBox_h.setSingleStep(0.1)
		self.doubleSpinBox_h.setProperty("value", 5.0)
		self.doubleSpinBox_h.setObjectName("doubleSpinBox_h")
		self.gridLayout.addWidget(self.doubleSpinBox_h, 3, 1, 1, 1)
		self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
		self.pushButton_update = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton_update.setObjectName("pushButton_update")
		self.gridLayout.addWidget(self.pushButton_update, 4, 0, 1, 2)
		self.doubleSpinBox_k1 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.doubleSpinBox_k1.setDecimals(1)
		self.doubleSpinBox_k1.setMinimum(0.1)
		self.doubleSpinBox_k1.setMaximum(10.0)
		self.doubleSpinBox_k1.setSingleStep(0.1)
		self.doubleSpinBox_k1.setProperty("value", 1.0)
		self.doubleSpinBox_k1.setObjectName("doubleSpinBox_k1")
		self.gridLayout.addWidget(self.doubleSpinBox_k1, 1, 1, 1, 1)
		self.doubleSpinBox_k2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.doubleSpinBox_k2.setDecimals(1)
		self.doubleSpinBox_k2.setMinimum(0.1)
		self.doubleSpinBox_k2.setMaximum(10.0)
		self.doubleSpinBox_k2.setSingleStep(0.1)
		self.doubleSpinBox_k2.setProperty("value", 1.0)
		self.doubleSpinBox_k2.setObjectName("doubleSpinBox_k2")
		self.gridLayout.addWidget(self.doubleSpinBox_k2, 2, 1, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
	
		self.retranslateUi()
	
	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "Proxy circle parameters"))
		self.label_4.setText(_translate("Form", "Height"))
		self.label_3.setText(_translate("Form", "   K_2"))
		self.pushButton_update.setText(_translate("Form", "Update"))
		self.label_2.setText(_translate("Form", "   K_1"))
		self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Proxy circle</span></p></body></html>"))
	
	def get_surface_params(self):
		params = {'k1': self.doubleSpinBox_k1.value(), 'k2': self.doubleSpinBox_k2.value(), 'h': self.doubleSpinBox_h.value()}
		return params
		
	def closeEvent(self, event):
		self.close()