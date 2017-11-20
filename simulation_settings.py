# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulation_settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.insert(0, 'C:/Users/Panni/thesis_in_Python/thesis/UI')
from cone_params import *
from cylinder_params import *
from paraboloid_params import *
from proxy_circle_params import *
from sphere_params import *
from torus_params import *
from light_source_settings import *
from main import *
from win32api import GetSystemMetrics


class Simulation_Settings(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.surface_window = None
		self.light_sources_window = None
		self.main_window = None
		self.setupUi()
		self.chosen_surface = self.radioButton_cyl
		self.radioButton_cyl.setChecked(True)
		
		self.radioButton_con.toggled.connect(self.on_radio_button_toggled)
		self.radioButton_pla.toggled.connect(self.on_radio_button_toggled)
		self.radioButton_sph.toggled.connect(self.on_radio_button_toggled)
		#self.radioButton_new.toggled.connect(self.on_radio_button_toggled)
		self.radioButton_pro.toggled.connect(self.on_radio_button_toggled)
		self.radioButton_cyl.toggled.connect(self.on_radio_button_toggled)
		self.radioButton_par.toggled.connect(self.on_radio_button_toggled)
		self.radioButton_tor.toggled.connect(self.on_radio_button_toggled)
		
		self.pushButton_start.clicked.connect(self.start_simulation)
		
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
		#self.radioButton_new = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
		#self.radioButton_new.setObjectName("radioButton_new")
		#self.gridLayout_3.addWidget(self.radioButton_new, 4, 1, 1, 1)
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
		self.setWindowTitle(_translate("Form", "Main - Simulation Settings"))
		self.pushButton_start.setText(_translate("Form", "Start"))
		self.label_7.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Select parametric surface</span></p></body></html>"))
		self.radioButton_con.setText(_translate("Form", "Cone"))
		self.radioButton_pla.setText(_translate("Form", "Plane"))
		self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Simulation Settings</span></p></body></html>"))
		self.radioButton_sph.setText(_translate("Form", "Sphere"))
		#self.radioButton_new.setText(_translate("Form", "New"))
		self.radioButton_pro.setText(_translate("Form", "Proxy_Circle"))
		self.radioButton_cyl.setText(_translate("Form", "Cylinder"))
		self.radioButton_par.setText(_translate("Form", "Paraboloid"))
		self.radioButton_tor.setText(_translate("Form", "Torus"))
		self.label.setText(_translate("Form", "Total photon number"))
		self.label_2.setText(_translate("Form", "Minimum photon power"))
		
	def on_radio_button_toggled(self):
		self.chosen_surface = self.sender()
		if self.chosen_surface.isChecked():
			print("Selected surface is %s" % (self.chosen_surface.text()))
			
	def start_simulation(self):
		self.setGeometry(1, 38, 301, 333)
		
		min_pow = self.doubleSpinBox_minpow.value()
		max_photon = self.spinBox_totpho.value()
		surface = self.chosen_surface.text()
		
		surface_window_name = surface + "_Parameters()"
		if surface != 'Plane' and surface != 'New':
			self.surface_window = eval(surface_window_name)
			self.surface_window.show()
		else:
			self.surface_window = None
		
		self.main_window = Main(surface)
		self.main_window.set_min_photon_power(min_pow)
		self.main_window.set_max_photon(max_photon)
		self.main_window.show()
		
		self.light_sources_window = Light_Source_Settings(self.main_window.light_sources, self.main_window.lightsource_num)
		self.light_sources_window.show()
	
		if self.surface_window is not None:
			self.surface_window.pushButton_update.clicked.connect(self.send_updated_surface)
			
		self.light_sources_window.pushButton_add_new.clicked.connect(self.main_window.add_new_lightsource)
		
		for i in range(self.main_window.lightsource_num):
			self.light_sources_window.pushButton_modify[i].clicked.connect(lambda: self.send_updated_ls(i))
	
		for i in range(self.main_window.lightsource_num):
			self.light_sources_window.pushButton_delete[i].clicked.connect(lambda: self.send_deleted_ls(i))
			
	def send_updated_ls(self, i):
		print i
		params = self.light_sources_window.get_ls_params(i)
		self.main_window.update_ls(i, params)
	
	def send_deleted_ls(self, i):
		self.main_window.delete_ls(i)
		
	def add_new_lightsource(self):
		self.main_window.add_new_lightsource()
		
		self.light_sources_window = Light_Source_Settings(self.main_window.light_sources, self.main_window.lightsource_num)
		self.light_sources_window.show()	
		
	def send_updated_surface(self):
		params = self.surface_window.get_surface_params()
		self.main_window.update_surface(params)
		
	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.closeEvent(e)
			
	def closeEvent(self, event):
		if self.surface_window is not None:
			self.surface_window.closeEvent(event)
		if self.light_sources_window is not None:
			self.light_sources_window.closeEvent(event)
		if self.main_window is not None:		
			self.main_window.closeEvent(event)
		self.close()
	
app = QtWidgets.QApplication(sys.argv)

screen = Simulation_Settings()
screen.show()
sys.exit(app.exec_())