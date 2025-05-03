import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QVBoxLayout, QGroupBox, QCheckBox, QSpinBox, QMessageBox, QListWidget, QListWidgetItem, QScrollArea
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
from FPIBGConfig import *
from FPIBGLog import *
from CfgLabel import *
import datetime


class TabFormConfig(QTabWidget):
    """ Object for the General Configuration Tab. This contains a form which allows the user to enter the specifications they would like to use for the simulation. """

    dictTab = []
    tabCount = 0
    layouts = []
    lyCount = 0
    objArry = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def doItems(self,cfg):
        for k ,v in cfg.items():
            if type(v) == list    :
                print("List",k,len(v))
            elif type(v) == str    :
                print("Str",k,len(v))
                widget = CfgString(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.cfg))
                self.objArry.append(widget)
            elif type(v) == bool    :
                print("Str",k,v)
                widget = CfgBool(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.cfg))
                self.objArry.append(widget)
            elif type(v) == int    :
                print("int",k,v)
                widget = CfgInt(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.cfg))
                self.objArry.append(widget)    
            elif type(v) == tuple   :
                print("tuple",k,len(v))
                widget = CfgArray(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.cfg))
           
    
    def nested(self,cfg):
        for k ,v in cfg.items():
            if type(v) == libconf.AttrDict:
                print("Dictionary:",k)
                self.tabCount+=1
                self.lyCount +=1
                self.dictTab.append(QScrollArea())
                root_name =  k
                self.tabs.addTab(self.dictTab[self.tabCount],root_name)
                content_widget = QWidget()
                content_widget.setStyleSheet('background-color: 111111;')
                self.dictTab[self.tabCount].setWidget(content_widget)
                self.layouts.append(QVBoxLayout(content_widget))
                self.dictTab[self.tabCount].setWidgetResizable(True)
                self.doItems(v)
                
           
    def createTab(self):
        pass


    def Create(self, FPIBGBase):
        """ Constructor for the TabGenConfig object, which sets up the form on the tab. """
        # Create Base member variables
        self.tabCount = 0
        self.lyCount = 0
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg
        self.log = self.bobj.log.log

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.dictTab.append(QScrollArea())
        root_name =  self.cfg.CfgFileName
        self.tabs.addTab(self.dictTab[self.tabCount],root_name)
        content_widget = QWidget()
        content_widget.setStyleSheet('background-color: 111111;')
        self.dictTab[self.tabCount].setWidget(content_widget)
        self.layouts.append(QVBoxLayout(content_widget))
        self.dictTab[self.tabCount].setWidgetResizable(True)
        
        self.doItems(self.cfg.config)
        self.nested(self.cfg.config)
        self.layout.addWidget(self.tabs)
        

       
        
        
