import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit,QListWidget
from PyQt6.QtWidgets import QDateEdit, QPushButton,QLabel, QGroupBox,QVBoxLayout,QHBoxLayout, QTextEdit,QRadioButton,QFileDialog,QFontComboBox
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap,QImage,QFontMetrics,QFont
from PIL import Image,ImageFile
from FPIBGclient import *
from FPIBGServer import *
from _thread import *
from PIL.ImageQt import ImageQt
import threading
from io import BytesIO
from pyqtLED import QtLed
import math
import libconf

class CfgString():

	key = ""
	value = ""
	def __init__(self, key,value):
		self.key = key
		self.value = value
  	
	def setSize(self,control,H,W):
		control.setMinimumHeight(H)
		control.setMinimumWidth(W)
		control.setMaximumHeight(H)
		control.setMaximumWidth(W)

	def Create(self,FPIBConfig):
		
		self.cfg = FPIBConfig
		
		self.font = QFont("Times", 12)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		paramgrp = QGroupBox("")
		paramlo = QGridLayout()
		paramgrp.setLayout(paramlo)
		
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,lwidth) 
		paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
		
		self.EditObj =  QLineEdit()
		self.EditObj.setFont(self.font)
		self.EditObj.setStyleSheet("background-color:  #aaaaaa")
		self.EditObj.setText(self.value)
		self.EditObj.editingFinished.connect(self.valueChange)
		#self.EditObj.textChanged.connect(self.valueChange)
		ewidth =  math.floor(metrics.horizontalAdvance(self.value)*1.25)
		self.setSize(self.EditObj,20,ewidth) 
		paramlo.addWidget(self.EditObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)
		#self.EditObj.   valueChange.connect(self.valueChanged)
		self.setSize(paramgrp,50,25+ewidth+lwidth)
		return paramgrp
		
	def valueChange(self):
		
		if(self.value!=self.EditObj.text()):
			print("Value Changed",self.key)
			self.cfg.config[self.key]=self.EditObj.text()
			#self.cfg.updateCfg()
		
		

class CfgInt():

	key = ""
	value = ""
	def __init__(self, key,value):
		self.key = key
		self.value = value
  	
	def setSize(self,control,H,W):
		control.setMinimumHeight(H)
		control.setMinimumWidth(W)
		control.setMaximumHeight(H)
		control.setMaximumWidth(W)

	def Create(self,FPIBConfig):
		
		self.cfg = FPIBConfig
		
		self.font = QFont("Times", 12)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		paramgrp = QGroupBox("")
		paramlo = QGridLayout()
		paramgrp.setLayout(paramlo)
		
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,lwidth) 
		paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
		
		self.EditObj =  QLineEdit()
		self.EditObj.setFont(self.font)
		self.EditObj.setStyleSheet("background-color:  #aaaaaa")
		self.EditObj.setText(str(self.value))
		self.EditObj.editingFinished.connect(self.valueChange)
		#self.EditObj.textChanged.connect(self.valueChange)
		ewidth =  math.floor(metrics.horizontalAdvance(str(self.value))*1.25)
		self.setSize(self.EditObj,20,ewidth) 
		paramlo.addWidget(self.EditObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)
		#self.EditObj.   valueChange.connect(self.valueChanged)
		self.setSize(paramgrp,50,25+ewidth+lwidth)
		return paramgrp
		
	def valueChange(self):
		
		if(str(self.value)!=self.EditObj.text()):
			print("Value Changed",self.key)
			self.cfg.config[self.key]=self.EditObj.text()
			#self.cfg.updateCfg()
		
		

