import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt
from TabFormGenConfig import *
from TabFormGenVPerf import *
from TabFormReports import *
from TabFormRunRpt import *
from TabFormRunSim import *
from TabFormSetUp import *

class TabObj(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.tabFormGenConfig = TabGenConfig()
        self.tabFormGenVPerf = TabGenVPerf()
        self.tabFormReports = TabReports()
        self.tabFormRunRpt = TabRunRpt()
        self.tabFormRunSim = TabRunSim()
        self.tabFormSetup = TabSetup()


    def SetForm(self):
        # personal page
       
        self.addTab(self.tabFormGenConfig, 'General Configuration')
        self.addTab(self.tabFormGenVPerf, 'Verification and Performance Testing')
        self.addTab(self.tabFormReports, 'Reports')
        self.addTab(self.tabFormRunRpt, 'Run')
        self.addTab(self.tabFormRunSim, 'Run Simulation Movie')
        self.addTab(self.tabFormSetup, 'Setup')