# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_new_ls.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Add_New_LS(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setupUi()
		
	def setupUi(self):
		self.setObjectName("Form")
		self.resize(324, 151)
		self.gridLayoutWidget = QtWidgets.QWidget(self)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 301, 131))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_4.setObjectName("label_4")
		self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
		self.doubleSpinBox_ypos = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.doubleSpinBox_ypos.setMaximum(1.0)
		self.doubleSpinBox_ypos.setSingleStep(0.1)
		self.doubleSpinBox_ypos.setProperty("value", 0.5)
		self.doubleSpinBox_ypos.setObjectName("doubleSpinBox_ypos")
		self.gridLayout.addWidget(self.doubleSpinBox_ypos, 1, 3, 1, 1)
		self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
		self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_5.setObjectName("label_5")
		self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
		self.doubleSpinBox_pow = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.doubleSpinBox_pow.setMaximum(1.0)
		self.doubleSpinBox_pow.setSingleStep(0.1)
		self.doubleSpinBox_pow.setProperty("value", 1.0)
		self.doubleSpinBox_pow.setObjectName("doubleSpinBox_pow")
		self.gridLayout.addWidget(self.doubleSpinBox_pow, 2, 3, 1, 1)
		self.pushButton_add = QtWidgets.QPushButton(self.gridLayoutWidget)
		self.pushButton_add.setObjectName("pushButton_add")
		self.gridLayout.addWidget(self.pushButton_add, 3, 0, 1, 4)
		self.spinBox_ppf = QtWidgets.QSpinBox(self.gridLayoutWidget)
		self.spinBox_ppf.setMaximum(2048)
		self.spinBox_ppf.setProperty("value", 512)
		self.spinBox_ppf.setObjectName("spinBox_ppf")
		self.gridLayout.addWidget(self.spinBox_ppf, 2, 1, 1, 1)
		self.doubleSpinBox_xpos = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.doubleSpinBox_xpos.setMaximum(1.0)
		self.doubleSpinBox_xpos.setSingleStep(0.1)
		self.doubleSpinBox_xpos.setProperty("value", 0.5)
		self.doubleSpinBox_xpos.setObjectName("doubleSpinBox_xpos")
		self.gridLayout.addWidget(self.doubleSpinBox_xpos, 1, 1, 1, 1)
		self.label = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label.setMaximumSize(QtCore.QSize(16777215, 16770000))
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
	
		self.retranslateUi()
	
	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("Form", "New Light Source"))
		self.label_4.setText(_translate("Form", "Photons per frame"))
		self.label_3.setText(_translate("Form", "  y  "))
		self.label_2.setText(_translate("Form", "  x  "))
		self.label_5.setText(_translate("Form", "Power"))
		self.pushButton_add.setText(_translate("Form", "Add"))
		self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Add new light source</span></p></body></html>"))
	
'''app = QtWidgets.QApplication(sys.argv)

screen = Add_New_LS()
screen.show()
sys.exit(app.exec_())'''