# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulation_settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys


class Simulation_Settings(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setupUi()
		
	def setupUi(self):
		self.setObjectName("Form")
		self.resize(301, 333)
		self.gridLayoutWidget_3 = QtWidgets.QWidget(self)
		self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 281, 311))
		self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
		self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
		self.pushButton.setObjectName("pushButton")
		self.gridLayout_3.addWidget(self.pushButton, 8, 0, 1, 2)
		self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label_7.setObjectName("label_7")
		self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 2)
		self.radioButton_5 = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_5.setObjectName("radioButton_5")
		self.gridLayout_3.addWidget(self.radioButton_5, 2, 0, 1, 1)
		self.radioButton = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton.setObjectName("radioButton")
		self.gridLayout_3.addWidget(self.radioButton, 1, 1, 1, 1)
		self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label_5.setObjectName("label_5")
		self.gridLayout_3.addWidget(self.label_5, 5, 0, 1, 2)
		self.radioButton_2 = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_2.setObjectName("radioButton_2")
		self.gridLayout_3.addWidget(self.radioButton_2, 3, 1, 1, 1)
		self.radioButton_7 = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_7.setObjectName("radioButton_7")
		self.gridLayout_3.addWidget(self.radioButton_7, 4, 1, 1, 1)
		self.radioButton_8 = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_8.setObjectName("radioButton_8")
		self.gridLayout_3.addWidget(self.radioButton_8, 3, 0, 1, 1)
		self.radioButton_6 = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_6.setObjectName("radioButton_6")
		self.gridLayout_3.addWidget(self.radioButton_6, 1, 0, 1, 1)
		self.radioButton_3 = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_3.setObjectName("radioButton_3")
		self.gridLayout_3.addWidget(self.radioButton_3, 4, 0, 1, 1)
		self.radioButton_4 = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_4.setObjectName("radioButton_4")
		self.gridLayout_3.addWidget(self.radioButton_4, 2, 1, 1, 1)
		self.spinBox = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
		self.spinBox.setMaximum(1048576)
		self.spinBox.setProperty("value", 524288)
		self.spinBox.setObjectName("spinBox")
		self.gridLayout_3.addWidget(self.spinBox, 6, 1, 1, 1)
		self.label = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label.setObjectName("label")
		self.gridLayout_3.addWidget(self.label, 6, 0, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label_2.setObjectName("label_2")
		self.gridLayout_3.addWidget(self.label_2, 7, 0, 1, 1)
		self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
		self.doubleSpinBox.setDecimals(3)
		self.doubleSpinBox.setMinimum(0.0)
		self.doubleSpinBox.setMaximum(1.0)
		self.doubleSpinBox.setSingleStep(0.01)
		self.doubleSpinBox.setProperty("value", 0.03)
		self.doubleSpinBox.setObjectName("doubleSpinBox")
		self.gridLayout_3.addWidget(self.doubleSpinBox, 7, 1, 1, 1)
	
		self.retranslateUi()
	
	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "Simulation Settings"))
		self.pushButton.setText(_translate("Form", "Start"))
		self.label_7.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Select parametric surface</span></p></body></html>"))
		self.radioButton_5.setText(_translate("Form", "Cone"))
		self.radioButton.setText(_translate("Form", "Plane"))
		self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Simulation Settings</span></p></body></html>"))
		self.radioButton_2.setText(_translate("Form", "Sphere"))
		self.radioButton_7.setText(_translate("Form", "New"))
		self.radioButton_8.setText(_translate("Form", "Proxy circle"))
		self.radioButton_6.setText(_translate("Form", "Cylinder"))
		self.radioButton_3.setText(_translate("Form", "Paraboloid"))
		self.radioButton_4.setText(_translate("Form", "Torus"))
		self.label.setText(_translate("Form", "Total photon number"))
		self.label_2.setText(_translate("Form", "Minimum photon power"))
	
app = QApplication(sys.argv)

screen = Simulation_Settings()
screen.show()
sys.exit(app.exec_())		