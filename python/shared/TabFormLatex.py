import sys
from PyQt6.QtWidgets import QFileDialog, QGroupBox,QMessageBox
from PyQt6.QtWidgets import QGridLayout, QTabWidget, QLineEdit,QListWidget
from PyQt6.QtWidgets import QPushButton, QGroupBox
from PyQt6 import QtCore
from FPIBGclient import *
from FPIBGServer import *
from _thread import *
from FPIBGConfig import FPIBGConfig
from LatexClass import *
from CfgLabel import *
from FPIBGException import *
from LatexSingleImage import *
from LatexMultiImage import *
from LatexSinglePlot import *
from LatexSinglePlotParticle import *
from LatexSingleTable import *

class TabFormLatex(QTabWidget):
    
    texFolder = ""
    CfgFile = ""
    texFileName = ""
    hasConfig = False
    itemcfg = FPIBGConfig("Latex Class")
    startDir = "J:/MOD/FPIBGUtility/Latex"
    startDir = "J:/FPIBGJournalStaticV2/rpt"
    startDir = "J:/FPIBGJournalStaticV2/cfg"

    ObjName = ""
    ltxObj = None

    def __init__(self, FPIBGBase, ObjName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.log.logs(self,"TabFormLatex finished init.")
    
    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    def SaveConfigurationFile(self):
        self.ltxObj.updateCfgData()
        
        #self.ltxObj.clearConfigGrp()

  
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        #folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        folder = QFileDialog.getOpenFileName(self, ("Open File"),
                                       self.startDir,
                                       ("Configuration File (*.cfg)"))
        
        if folder[0]:
            self.CfgFile = folder[0]
            self.texFolder = os.path.dirname(self.CfgFile)
            self.texFileName = os.path.splitext(os.path.basename(self.CfgFile))[0]
            self.dirEdit.setText(self.CfgFile)
            self.itemcfg = FPIBGConfig(self.CfgFile)
            self.itemcfg.Create(self.bobj.log,self.CfgFile)
            self.type = self.itemcfg.config.type_text 
            self.imgmgrp = QGroupBox("Image Interface")
            self.setSize(self.imgmgrp,20,20)
            self.tab_layout.addWidget(self.imgmgrp,0,3,2,2)
            if self.hasConfig == True:
                self.ltxObj.clearConfigGrp()
            if "multiimage" in self.type:
                self.ltxObj = LatexMultiImage(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.ltxObj.setImgGroup()
                self.ListObj.setEnabled(False)
                self.hasConfig = True
                
            elif "image" in self.type:
                self.ltxObj = LatexSingleImage(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.setImgGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "singletable" in self.type:
                self.ltxObj = LatexSingleTable(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.setImgGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "singleplotparticle" in self.type:
                self.ltxObj = LatexSinglePlotParicle(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "singleplot" in self.type:
                self.ltxObj = LatexSinglePlot(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "type" in self.type:
                self.ltxObj = LatexSingleImage(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.setImgGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            else:
                print("InvalidType")
                return
    
    def browseNewItem(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        #folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if(self.ListObj.currentRow() < 0):
            print("Must select type first.")
            return
        else:
            print(f"Opening Row {self.ListObj.currentRow()}")

        folder = QFileDialog.getSaveFileName(self, ("Open File"),
                                       "J:/FPIBGJournalStaticV2/rpt",
                                       ("Images (*.cfg)"))
        cfg_cnt = ""
        if folder[0]:
            self.CfgFile = folder[0]
            with open(self.cfg.single_template, 'r') as file:
                cfg_cnt = file.read()
            print(cfg_cnt)
            file.close()
            with open(folder[0], 'w') as file:
                file.write(cfg_cnt)
                file.close()
            self.texFolder = os.path.dirname(self.CfgFile)
            self.texFileName = os.path.splitext(os.path.basename(self.CfgFile))[0]
            self.dirEdit.setText(self.CfgFile)
            self.OpenLatxCFG(self.CfgFile)
   
    def Create(self):
        self.log.logs(self,"TabFormLatex started Create.")
        #try:
        self.setStyleSheet("background-color:  #eeeeee")
        self.tab_layout = QGridLayout()
        self.tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.tab_layout)

        ## -------------------------------------------------------------
        ## Set parent directory
        LatexcfgFile = QGroupBox("Latex File Configuration")
        self.setSize(LatexcfgFile,200,300)
        self.tab_layout.addWidget(LatexcfgFile,0,0,1,2,alignment= Qt.AlignmentFlag.AlignLeft)
        
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
        self.SaveButton.clicked.connect(self.SaveConfigurationFile)
        dirgrid.addWidget(self.SaveButton,2,0)

        self.newButton = QPushButton("New")
        self.setSize(self.SaveButton,30,100)
        self.newButton.setStyleSheet("background-color:  #dddddd")
        self.newButton.clicked.connect(self.browseNewItem)
        dirgrid.addWidget(self.newButton,2,1)

        self.ListObj =  QListWidget()
        #self.ListObj.setFont(self.font)
        self.ListObj.setStyleSheet("background-color:  #FFFFFF")
        self.vcnt = 0            
        self.ListObj.insertItem(0, "image")
        self.ListObj.insertItem(1, "plot")
        self.ListObj.insertItem(2, "multiplot")
        self.ListObj.insertItem(3, "multiimage")
        self.ListObj.itemSelectionChanged.connect(lambda: self.valueChangeArray(self.ListObj))
        dirgrid.addWidget(self.ListObj,3,0,1,2)
        self.log.logs(self,"TabFormLatex finished Create.")
       # except Exception as inst:
       #     print(f"{self.ObjName}: Error: {inst.args}")
       #     self.log.logs(self,"error")

    def valueChangeArray(self,listObj):  
        selected_items = listObj.selectedItems()
        if selected_items:
            print("List object Value Changed",selected_items[0].text())
            self.ltxObj.setTypeText(selected_items[0].text())         
    