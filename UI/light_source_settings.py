# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'light_source_settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Light_Source_Settings(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setupUi()
		
	def setupUi(self):
		self.setObjectName("Form")
		self.resize(325, 855)
		self.gridLayoutWidget = QtWidgets.QWidget(self)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 301, 311))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.minimap = QtWidgets.QGraphicsView(self.gridLayoutWidget)
		self.minimap.setObjectName("minimap")
		self.gridLayout.addWidget(self.minimap, 1, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
		self.pushButton_add_new = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton_add_new.setObjectName("pushButton_add_new")
		self.gridLayout.addWidget(self.pushButton_add_new, 2, 0, 1, 1)
		self.verticalLayoutWidget = QtWidgets.QWidget(self)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 330, 301, 511))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
	
		self.retranslateUi()
	
	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "Light Source Settings"))
		self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Light Sources</span></p></body></html>"))
		self.pushButton_add_new.setText(_translate("Form", "Add new"))
	
'''app = QtWidgets.QApplication(sys.argv)

screen = Light_Source_Settings()
screen.show()
sys.exit(app.exec_())'''