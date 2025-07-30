import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt

from TabFormWelcome import *
from gpu_2DTab import *
from TabFormPlotOnly import *
## Add all tabs
class GPUTabs(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        

    ## Add all tabs to this tab form (parent)
    def Create(self,FPIBGBase):
        self.bobj = FPIBGBase
        ## Create the tabs
        self.tabFormWelcome = TabFormWelcome()
        self.tabPlot = TabPlotOnly()
       
        ## Add the tabs to tabs to this tab container.
        self.addTab(self.tabPlot, 'Study Tab')
        self.addTab(self.tabFormWelcome, 'Welcome')
        

        ## Call set form to 
        self.tabFormWelcome.Create()
        self.tabPlot.Create(FPIBGBase)