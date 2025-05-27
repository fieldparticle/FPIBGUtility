import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit,QListWidget,QComboBox
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

class CfgArray():
	def __init__(self, key,value):
		self.key = key
		self.value = value
  	
	def setSize(self,control,H,W):
		control.setMinimumHeight(H)
		control.setMinimumWidth(W)
		control.setMaximumHeight(H)
		control.setMaximumWidth(W)

	def getListItemText(self):
		selected_items = self.ListObj.selectedItems()
		if selected_items:
			print(f"returning {selected_items[0].text()}\n")
			return selected_items[0].text()
			
		

	def Create(self,config,FPIBGConfig,parent):
		self.cfg = config
		self.base = FPIBGConfig
		
			
		self.font = QFont("Times", 10)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		self.paramgrp = QGroupBox("")
		paramlo = QGridLayout()
		self.paramgrp.setLayout(paramlo)
		self.paramgrp.setStyleSheet('background-color: 111111;')
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		self.lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,self.lwidth) 
		paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)

		self.ListObj =  QListWidget()
		self.ListObj.setFont(self.font)
		self.ListObj.setStyleSheet("background-color:  #FFFFFF")
		self.vcnt = 0
		for v in self.value:
			self.ListObj.insertItem(self.vcnt,self.value[self.vcnt])
			self.vcnt+=1
#			self.ListObj.editingFinished.connect(self.valueChange)
			
			#self.LabelObj.setFont(self.font)
			#lwidth = metrics.horizontalAdvance(v)
			#ewidth =  math.floor(metrics.horizontalAdvance(self.value)*1.25)
			#self.setSize(self.ListObj,20,ewidth) 
			paramlo.addWidget(self.ListObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)

		self.ListObj.itemSelectionChanged.connect(lambda: parent.valueChangeArray(self.ListObj))
		#self.setSize(paramgrp,50,25+ewidth+lwidth)
		return self.paramgrp
		
	def valueChange(self):
		selected_items = self.ListObj.selectedItems()
		if selected_items:
			print("Value Changed",selected_items[0].text())
	#		self.cfg[self.key]=self.EditObj.text()
			#self.base.updateCfg()

	def getHW(self):
		H = self.vcnt*20
		W = 300
		return H,W

	def setHW(self,H,W):
		self.setSize(self.ListObj,H,W)
		Hg = H+20
		Wg = W+20+self.lwidth
		self.setSize(self.paramgrp,Hg,Wg)
		return Hg,Wg
		
		
		
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

	def Create(self,config,FPIBGConfig):
		
		self.cfg = config
		self.base = FPIBGConfig
		
		self.font = QFont("Times", 10)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		self.paramgrp = QGroupBox("")
		paramlo = QGridLayout()
		self.paramgrp.setLayout(paramlo)
		self.paramgrp.setStyleSheet('background-color: 111111;')
		
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		self.lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,self.lwidth) 
		paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
		
		self.EditObj =  QLineEdit()
		self.EditObj.setFont(self.font)
		self.EditObj.setStyleSheet("background-color:  #FFFFFF")
		self.EditObj.setText(self.value)
		self.EditObj.editingFinished.connect(self.valueChange)
		#self.EditObj.textChanged.connect(self.valueChange)
		ewidth =  math.floor(metrics.horizontalAdvance(self.value)*1.25)
		if len(self.value) == 0:
			ewidth = 100
		self.setSize(self.EditObj,20,ewidth) 
		paramlo.addWidget(self.EditObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)
		#self.EditObj.   valueChange.connect(self.valueChanged)
		self.setSize(self.paramgrp,50,300)
		return self.paramgrp
	
	def setText(self,text):
		self.EditObj.setText(text) 

	def setHW(self,H,W):
		self.setSize(self.EditObj,H,W)
		Hg = H+20
		Wg = W+20+self.lwidth
		self.setSize(self.paramgrp,Hg,Wg)
		return Hg,Wg
		

	def valueChange(self):
		if(self.value!=self.EditObj.text()):
			print("Value Changed",self.key)
			self.cfg[self.key]=self.EditObj.text()
			#self.base.updateCfg()
		
		
class CfgTextBox():

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

	def Create(self,config,FPIBGConfig):
		
		self.cfg = config
		self.base = FPIBGConfig
		
		self.font = QFont("Times", 10)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		self.paramgrp = QGroupBox("")
		paramlo = QGridLayout()
		self.paramgrp.setLayout(paramlo)
		self.paramgrp.setStyleSheet('background-color: 111111;')
		
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		self.lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,self.lwidth) 
		paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
		
		self.EditObj =  QTextEdit()
		self.EditObj.setFont(self.font)
		self.EditObj.setStyleSheet("background-color:  #FFFFFF")
		self.EditObj.setText(self.value)
		self.EditObj.textChanged.connect(self.valueChange)
		#self.EditObj.textChanged.connect(self.valueChange)
		ewidth =  math.floor(metrics.horizontalAdvance(self.value)*1.25)
		if len(self.value) == 0:
			ewidth = 100
		self.setSize(self.EditObj,20,ewidth) 
		paramlo.addWidget(self.EditObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)
		#self.EditObj.   valueChange.connect(self.valueChanged)
		self.setSize(self.paramgrp,50,25+ewidth+self.lwidth)
		return self.paramgrp
	
	def setHW(self,H,W):
		self.setSize(self.EditObj,H,W)
		Hg = H+20
		Wg = W+20+self.lwidth
		self.setSize(self.paramgrp,Hg,Wg)
		return Hg,Wg

	def valueChange(self):
		if(self.value!=self.EditObj.toPlainText()):
			print("Value Changed",self.key)
			self.cfg[self.key]=self.EditObj.toPlainText()
			#self.base.updateCfg()
		
		


class CfgBool():

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

	def Create(self,config,FPIBGConfig):
		
		self.cfg = config
		self.base = FPIBGConfig
		
		self.font = QFont("Times", 12)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		paramgrp = QGroupBox("")
		paramlo = QGridLayout()
		paramgrp.setLayout(paramlo)
		paramgrp.setStyleSheet('background-color: 111111;')
		
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,lwidth) 
		paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
		
		self.Combo =  QComboBox()
		self.Combo.setFont(self.font)
		self.Combo.setStyleSheet("background-color:  #FFFFFF")
		
		self.Combo.addItem("true")
		self.Combo.addItem("false")
		#self.Combo.editingFinished.connect(self.valueChange)
		#self.Combo.textChanged.connect(self.valueChange)
		#ewidth =  math.floor(metrics.horizontalAdvance(self.value)*1.25)
		#self.setSize(self.Combo,20,ewidth) 
		paramlo.addWidget(self.Combo,0,1,alignment= Qt.AlignmentFlag.AlignLeft)
		#self.Combo.   valueChange.connect(self.valueChanged)
		#self.setSize(paramgrp,50,25+ewidth+lwidth)
		return paramgrp
		
	def valueChange(self):
		if(self.value!=self.Combo.text()):
			print("Value Changed",self.key)
			self.cfg[self.key]=self.Combo.text()
			#self.base.updateCfg()
		
		

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

	def Create(self,config,FPIBGConfig):
		
		self.cfg = config
		self.base = FPIBGConfig
		
		self.font = QFont("Times", 12)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		paramgrp = QGroupBox("")
		paramlo = QGridLayout()
		paramgrp.setLayout(paramlo)
		paramgrp.setStyleSheet('background-color: 111111;')
		
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,lwidth) 
		paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
		
		self.EditObj =  QLineEdit()
		self.EditObj.setFont(self.font)
		#self.EditObj.setStyleSheet('background-color: 222222;')
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
			self.cfg[self.key]=self.EditObj.text()
			self.base.updateCfg()
		
		

