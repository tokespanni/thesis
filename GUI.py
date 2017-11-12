from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import sys
from main import *

class Select_Surface(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		
		self.setWindowTitle('Setup window')
		self.lbl_intro = QLabel("")
		
		grid = QGridLayout()
		self.setLayout(grid)
		
		grid.addWidget(QLabel('Please choose parametric surface, or define one.'), 0,0)
		
		self.load_surfaces()
		
		self.radiobutton = None
		
		for i in range(len(self.surfaces)):		
			radiobutton = QRadioButton(self.surfaces[i])
			radiobutton.setChecked(False)
			radiobutton.name = self.surfaces[i]
			radiobutton.toggled.connect(self.on_radio_button_toggled)
			grid.addWidget(radiobutton, i+1, 0)
		
		self.ok_btn = QPushButton('Ok')
		
		grid.addWidget(self.ok_btn,len(self.surfaces)+1, 0)
		
		self.ok_btn.clicked.connect(lambda: self.ok_btn_clk(self.radiobutton.name, self.lbl_intro))
		
		grid.addWidget(self.lbl_intro, len(self.surfaces)+2, 0)
		self.show()

	def on_radio_button_toggled(self):
		self.radiobutton = self.sender()
		if self.radiobutton.isChecked():
			print("Selected surface is %s" % (self.radiobutton.name))
			
	def load_surfaces(self):
		with open('surfaces.txt', 'r') as f:
			self.surfaces = f.readlines()
		self.surfaces = [x.strip() for x in self.surfaces]
		
	def ok_btn_clk(self, surf, intro):
		if surf is None or surf == 'New':
			intro.setText('Please choose an existing surface.')
		else:
			self.mw = Main(surf)
			print 'ok'
			self.hide()
			self.mw.show()