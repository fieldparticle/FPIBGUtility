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

    tabs = []
    objArry = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    def nested(self,cfg):
        for k ,v in cfg.items():
            #print(k,v)
            if type(v) == libconf.AttrDict:
                pass # self.nested(v)
            elif type(v) == list    :
                print("List",k,len(v))
            elif type(v) == str    :
                print("Str",k,len(v))
                label = CfgString(k,v)
                self.flay.addWidget(label.Create(cfg))
                
                self.objArry.append(label)
            elif type(v) == dict    :
                print("dict",k,len(v))
            else:
                print("unk:",k)
            if(k=="application"):
                print("app:",type(k),type(v))
    
    def Create(self, FPIBGBase):
        """ Constructor for the TabGenConfig object, which sets up the form on the tab. """
        # Create Base member variables
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg
        self.log = self.bobj.log.log

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab2 = QScrollArea()
        self.tabs.addTab(self.tab2, 'Tab 2')
       
        content_widget = QWidget()
        self.tab2.setWidget(content_widget)
        self.flay = QVBoxLayout(content_widget)
        self.tab2.setWidgetResizable(True)
        self.nested(self.cfg.config)
        self.layout.addWidget(self.tabs)
        

       
        
        

    def top(self,cfg):
      
        for k ,v in cfg.items():
            if type(v) == list    :
                print("List",k,len(v))
            elif type(v) == str    :
                print("Str",k,len(v))
                label = CfgString(k,v)
                self.tablayout.addWidget(label.Create(cfg))
                self.objArry.append(label)
            elif type(v) == int    :
                page = CfgInt(k,v)
                self.tablayout.addWidget(page.Create(cfg))
                self.objArry.append(page)
            else:
                print("unk:",k)
            if(k=="application"):
                print("app:",type(k),type(v))
   