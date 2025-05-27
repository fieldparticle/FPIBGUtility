import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLineEdit,QListWidget,QComboBox
from PyQt6.QtWidgets import QPushButton,QLabel, QGroupBox, QTextEdit, QRadioButton,QFileDialog
from PyQt6 import QtCore
from PyQt6.QtGui import QImage,QFontMetrics,QFont
from _thread import *
from PIL.ImageQt import ImageQt
from pyqtLED import QtLed
import math


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
		self.Parent = parent
			
		self.font = QFont("Times", 10)
		self.font.setBold(False)

		metrics = QFontMetrics(self.font)

		self.paramgrp = QGroupBox("")
		self.paramlo = QGridLayout()
		self.paramgrp.setLayout(self.paramlo)
		self.paramgrp.setStyleSheet('background-color: 111111;')
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		self.lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,self.lwidth) 
		self.paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)

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
			self.paramlo.addWidget(self.ListObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)

		self.ListObj.itemSelectionChanged.connect(lambda: parent.valueChangeArray(self.ListObj))
		#self.setSize(paramgrp,50,25+ewidth+lwidth)
		return self.paramgrp
		
	def getLayout(self):
		return self.paramlo
	
	def valueChangeArray(self):
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
	EditObj = None
	dirFlg = False
	fileFlg = False
	H = 0
	W = 0

	def __init__(self, key,value,parent):
		self.key = key
		self.value = value
		self.Parent = parent

	def setAsDir(self):
		self.dirFlg = True

	def setAsFile(self):
		self.fileFlg = True

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
		
		ewidth =  math.floor(metrics.horizontalAdvance(self.value)*1.25)
		if len(self.value) == 0:
			ewidth = 100

		
		paramlo.addWidget(self.EditObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)
		
		if(self.fileFlg == True):
			self.dirButton = QPushButton("Select File")
			self.setSize(self.dirButton,30,100)
			self.dirButton.setStyleSheet("background-color:  #dddddd")
			self.dirButton.clicked.connect(self.AddImageItemFile)
			paramlo.addWidget(self.dirButton,1,0,alignment= Qt.AlignmentFlag.AlignLeft)
			self.H = 75
			self.W = 400
			self.setSize(self.EditObj,20,self.W-self.lwidth-20) 
			self.setSize(self.paramgrp,self.H,self.W)
		elif(self.dirFlg == True):
			self.dirButton = QPushButton("Select Dir")
			self.setSize(self.dirButton,30,100)
			self.dirButton.setStyleSheet("background-color:  #dddddd")
			self.dirButton.clicked.connect(self.AddImageItemDir)
			paramlo.addWidget(self.dirButton,1,0,alignment= Qt.AlignmentFlag.AlignLeft)
			self.H = 75
			self.W = 400
			self.setSize(self.EditObj,20,self.W-self.lwidth-20) 
			self.setSize(self.paramgrp,self.H,self.W)
		else:
			self.H = 50
			self.W = 400
			self.setSize(self.EditObj,20,self.W-self.lwidth-20) 
			self.setSize(self.paramgrp,self.H,self.W)
		return self.paramgrp
  	
	def RemoveImageItem(self):
		print("remove")

	def AddImageItemDir(self):
		folder = QFileDialog.getOpenFileName(self.paramgrp, ("Open File"),
                                       "J:/FPIBGJournalStaticV2/rpt",
                                       ("Images (*.png)"))
		
		if folder[0]:
			self.texFolder = os.path.dirname(folder[0])
			self.texFileName = os.path.splitext(os.path.basename(folder[0]))[0]
			self.EditObj.setText(self.texFolder)
			self.Parent.dirsChanged(folder[0])

	def AddImageItemFile(self):
		folder = QFileDialog.getOpenFileName(self.paramgrp, ("Open File"),
                                       "J:/FPIBGJournalStaticV2/rpt",
                                       ("Images (*.png)"))
		
		if folder[0]:
			self.texFolder = os.path.dirname(folder[0])
			self.texFileName = os.path.splitext(os.path.basename(folder[0]))[0]
			self.EditObj.setText(self.texFolder)
			self.Parent.filesChanged(folder[0])


	def AddImageItemDir(self):
		folder = QFileDialog.getExistingDirectory(self.paramgrp, ("Select Directory"),
                                       "J:/FPIBGJournalStaticV2/rpt")

		
		if folder:
			self.EditObj.setText(folder)
			


	def setText(self,text):
		self.EditObj.setText(text) 

	def setHW(self,H,W):
		#self.setSize(self.EditObj,H,W)
		#Hg = H+20
		#Wg = W+20+self.lwidth
		#self.setSize(self.paramgrp,Hg,Wg)
		return self.H,self.W
	
	def setTypeText(self,text):
		self.EditObj.setText(text)

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
		self.paramlo = QGridLayout()
		self.paramgrp.setLayout(self.paramlo)
		self.paramgrp.setStyleSheet('background-color: 111111;')
		
		text = self.key + ":"
		self.LabelObj = QLabel(text)
		self.LabelObj.setFont(self.font)
		self.lwidth = metrics.horizontalAdvance(text)
		self.setSize(self.LabelObj,20,self.lwidth) 
		self.paramlo.addWidget(self.LabelObj,0,0,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignAbsolute)
		
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
		self.paramlo.addWidget(self.EditObj,0,1,alignment= Qt.AlignmentFlag.AlignLeft)
		#self.EditObj.   valueChange.connect(self.valueChanged)
		self.setSize(self.paramgrp,50,25+ewidth+self.lwidth)
		return self.paramgrp
	
	def getLayout(self):
		return self.paramlo

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
		
		

