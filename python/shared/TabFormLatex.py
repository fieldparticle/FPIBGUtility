import sys
from PyQt6.QtWidgets import QFileDialog, QVBoxLayout, QGroupBox, QCheckBox, QSpinBox, QMessageBox, QListWidgetItem, QScrollArea
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit,QListWidget
from PyQt6.QtWidgets import QDateEdit, QPushButton,QLabel, QGroupBox,QVBoxLayout,QHBoxLayout, QTextEdit,QRadioButton,QFileDialog
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap,QImage
from PIL import Image,ImageFile
from FPIBGclient import *
from FPIBGServer import *
from _thread import *
from PIL.ImageQt import ImageQt
import threading
from io import BytesIO
from pyqtLED import QtLed
from FPIBGConfig import FPIBGConfig
from FPIBGPlotDataEXP import *
from LatexClass import *
from CfgLabel import *

class TabFormLatex(QTabWidget):
    
    texFolder = ""
    CfgFile = ""
    texFileName = ""
    LatexFileImage = LatexImage("LatexClass")
    itemcfg = FPIBGConfig("Latex Class")
    dictTab = []
    tabCount = 0
    layouts = []
    lyCount = 0
    objArry = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    def OpenLatxCFG(self,cfgFile):
        self.itemcfg = FPIBGConfig(cfgFile)
        self.itemcfg.Create(self.bobj.log,cfgFile)
        print(self.itemcfg)
        self.ImageName = self.itemcfg.config.images
        self.ImagePath = self.texFolder + "/" + self.ImageName
        self.pixmap = QPixmap(self.ImagePath)
        self.setSize(self.imgmgrp,self.pixmap.height()+20,self.pixmap.width()) 
        self.setSize(self.image,self.pixmap.height()+20,self.pixmap.width()) 
        self.image.setPixmap(self.pixmap)
        self.LatexFileImage.outDirectory = self.itemcfg.config.py_plots_dir
        self.LatexFileImage.ltxDirectory = self.itemcfg.config.latex_plots_dir
        self.Type = self.itemcfg.config.type
        self.doItems(self.itemcfg.config)
        

    def doItems(self,cfg):
        self.tabCount+=1
        self.lyCount +=1
        self.dictTab.append(QScrollArea())
        self.tabs.addTab(self.dictTab[self.tabCount],"Config Items")
        content_widget = QWidget()
        content_widget.setStyleSheet('background-color: 111111;')
        self.dictTab[self.tabCount].setWidget(content_widget)
        self.layouts.append(QVBoxLayout(content_widget))
        self.dictTab[self.tabCount].setWidgetResizable(True)
        
        for k ,v in cfg.items():
            if type(v) == list    :
                print("List",k,len(v))
            elif type(v) == str    :
                print("Str",k,len(v))
                widget = CfgString(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg.config))
                self.objArry.append(widget)
            elif type(v) == bool    :
                print("Str",k,v)
                widget = CfgBool(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg.config))
                self.objArry.append(widget)
            elif type(v) == int    :
                print("int",k,v)
                widget = CfgInt(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg.config))
                self.objArry.append(widget)    
            elif type(v) == tuple   :
                print("tuple",k,len(v))
                widget = CfgArray(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg.config))

        
            
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        #folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        folder = QFileDialog.getOpenFileName(self, ("Open File"),
                                       "J:/FPIBGJournalStaticV2/rpt",
                                       ("Images (*.cfg)"))
        
        if folder[0]:
            self.CfgFile = folder[0]
            self.texFolder = os.path.dirname(self.CfgFile)
            self.texFileName = os.path.splitext(os.path.basename(self.CfgFile))[0]
            self.dirEdit.setText(self.CfgFile)
            self.OpenLatxCFG(self.CfgFile)
            
            
    def save_latex_Image(self):
        self.LatexFileImage.Create(self.bobj,self.texFileName)
        self.LatexFileImage.cleanPRE = True
        self.LatexFileImage.caption =  self.itemcfg.config.caption
        self.LatexFileImage.width = 0
        self.LatexFileImage.height = 0
        self.LatexFileImage.title = "TITLE:spf v loaded p"
        self.LatexFileImage.scale = 0.3
        self.LatexFileImage.fontSize = 10
        self.LatexFileImage.float = False
        self.LatexFileImage.placement = "h"
        self.LatexFileImage.Write() 

    def Create(self,FPIBGBase):
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)

        ## -------------------------------------------------------------
        ## Set parent directory
        LatexcfgFile = QGroupBox("Latex File Configuration")
        self.setSize(LatexcfgFile,500,600)
        tab_layout.addWidget(LatexcfgFile,0,0,1,1,alignment= Qt.AlignmentFlag.AlignLeft)
        
        dirgrid = QGridLayout()
        LatexcfgFile.setLayout(dirgrid)

        self.dirEdit =  QLineEdit()
        self.dirEdit.setStyleSheet("background-color:  #ffffff")
        self.dirEdit.setText("")

        self.dirButton = QPushButton("Browse")
        self.setSize(self.dirButton,30,100)
        self.dirButton.setStyleSheet("background-color:  #dddddd")
        self.dirButton.clicked.connect(self.browseFolder)
        dirgrid.addWidget(self.dirButton,0,0)
        dirgrid.addWidget(self.dirEdit,0,1)

        self.SaveButton = QPushButton("Save")
        self.setSize(self.SaveButton,30,100)
        self.SaveButton.setStyleSheet("background-color:  #dddddd")
        self.SaveButton.clicked.connect(self.save_latex_Image)
        dirgrid.addWidget(self.SaveButton,2,0)
        

    

         ## -------------------------------------------------------------
        ## Image Interface
        self.imgmgrp = QGroupBox("Image Interface")
        self.setSize(self.imgmgrp,20,20)
        tab_layout.addWidget(self.imgmgrp,0,3,2,2)
        
        imagelo = QGridLayout()
        self.imgmgrp.setLayout(imagelo)

        self.image = QLabel()
        self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,15,15)
        imagelo.addWidget(self.image,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        #self.changeImage()
