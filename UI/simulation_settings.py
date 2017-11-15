# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulation_settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from add_new_ls import *
from cone_params import *
from cylinder_params import *
from nth_ls import *
from paraboloid_params import *
from proxy_circle_params import *
from sphere_params import *
from torus_params import *


class Simulation_Settings(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
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
		self.pushButton_start = QtWidgets.QPushButton(self.gridLayoutWidget_3)
		self.pushButton_start.setObjectName("pushButton_start")
		self.gridLayout_3.addWidget(self.pushButton_start, 8, 0, 1, 2)
		self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label_7.setObjectName("label_7")
		self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 2)
		self.radioButton_con = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_con.setObjectName("radioButton_con")
		self.gridLayout_3.addWidget(self.radioButton_con, 2, 0, 1, 1)
		self.radioButton_pla = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_pla.setObjectName("radioButton_pla")
		self.gridLayout_3.addWidget(self.radioButton_pla, 1, 1, 1, 1)
		self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label_5.setObjectName("label_5")
		self.gridLayout_3.addWidget(self.label_5, 5, 0, 1, 2)
		self.radioButton_sph = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_sph.setObjectName("radioButton_sph")
		self.gridLayout_3.addWidget(self.radioButton_sph, 3, 1, 1, 1)
		self.radioButton_new = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_new.setObjectName("radioButton_new")
		self.gridLayout_3.addWidget(self.radioButton_new, 4, 1, 1, 1)
		self.radioButton_pro = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_pro.setObjectName("radioButton_pro")
		self.gridLayout_3.addWidget(self.radioButton_pro, 3, 0, 1, 1)
		self.radioButton_cyl = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_cyl.setObjectName("radioButton_cyl")
		self.gridLayout_3.addWidget(self.radioButton_cyl, 1, 0, 1, 1)
		self.radioButton_par = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_par.setObjectName("radioButton_par")
		self.gridLayout_3.addWidget(self.radioButton_par, 4, 0, 1, 1)
		self.radioButton_tor = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		self.radioButton_tor.setObjectName("radioButton_tor")
		self.gridLayout_3.addWidget(self.radioButton_tor, 2, 1, 1, 1)
		self.spinBox_totpho = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
		self.spinBox_totpho.setMaximum(1048576)
		self.spinBox_totpho.setProperty("value", 524288)
		self.spinBox_totpho.setObjectName("spinBox_totpho")
		self.gridLayout_3.addWidget(self.spinBox_totpho, 6, 1, 1, 1)
		self.label = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label.setObjectName("label")
		self.gridLayout_3.addWidget(self.label, 6, 0, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label_2.setObjectName("label_2")
		self.gridLayout_3.addWidget(self.label_2, 7, 0, 1, 1)
		self.doubleSpinBox_minpow = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
		self.doubleSpinBox_minpow.setDecimals(3)
		self.doubleSpinBox_minpow.setMinimum(0.0)
		self.doubleSpinBox_minpow.setMaximum(1.0)
		self.doubleSpinBox_minpow.setSingleStep(0.01)
		self.doubleSpinBox_minpow.setProperty("value", 0.03)
		self.doubleSpinBox_minpow.setObjectName("doubleSpinBox_minpow")
		self.gridLayout_3.addWidget(self.doubleSpinBox_minpow, 7, 1, 1, 1)
	
		self.retranslateUi()
	
	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "Simulation Settings"))
		self.pushButton_start.setText(_translate("Form", "Start"))
		self.label_7.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Select parametric surface</span></p></body></html>"))
		self.radioButton_con.setText(_translate("Form", "Cone"))
		self.radioButton_pla.setText(_translate("Form", "Plane"))
		self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Simulation Settings</span></p></body></html>"))
		self.radioButton_sph.setText(_translate("Form", "Sphere"))
		self.radioButton_new.setText(_translate("Form", "New"))
		self.radioButton_pro.setText(_translate("Form", "Proxy circle"))
		self.radioButton_cyl.setText(_translate("Form", "Cylinder"))
		self.radioButton_par.setText(_translate("Form", "Paraboloid"))
		self.radioButton_tor.setText(_translate("Form", "Torus"))
		self.label.setText(_translate("Form", "Total photon number"))
		self.label_2.setText(_translate("Form", "Minimum photon power"))
		
	def get_settings(self):
		self.
	
app = QtWidgets.QApplication(sys.argv)

screen = Simulation_Settings()
screen.show()
sys.exit(app.exec_())