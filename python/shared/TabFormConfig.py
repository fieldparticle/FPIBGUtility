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
                self.main_layout.addWidget(label.Create(cfg))
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
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold your main layout
        scroll_widget = QWidget()
        self.main_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        main_window_layout = QVBoxLayout(self)
        main_window_layout.addWidget(scroll_area)
        self.setLayout(main_window_layout)

        self.nested(self.cfg.config)
        


        
        # self.setLayout(main_layout)

        #self.populate()

   