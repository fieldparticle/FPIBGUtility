import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt
from TabFormGenConfig import *
from TabFormGenVPerf import *
from TabFormReports import *
from TabFormRunRpt import *
from TabFormRunSim import *
from TabFormSetUp import *
from TabFormWelcome import *
from TabFormGenData import *
from TabFormGenSimPlots import *
## Add all tabs
class TabObj(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        

    ## Add all tabs to this tab form (parent)
    def Create(self,FPIBGBase):
        self.bobj = FPIBGBase
        ## Create the tabs
        self.tabFormWelcome = TabFormWelcome()
        self.tabFormGenConfig = TabGenConfig()
        self.tabFormGenVPerf = TabGenVPerf()
        self.tabFormReports = TabReports()
        self.tabFormRunRpt = TabRunRpt()
        self.tabFormRunSim = TabRunSim()
        self.tabFormSetup = TabSetup()
        self.tabFormGenData = TabGenData()        
        self.tabFormSimPlots = TabSimPlots()        

        ## Add the tabs to tabs to this tab container.
        self.addTab(self.tabFormWelcome, 'Welcome')
        self.addTab(self.tabFormGenConfig, 'General Configuration')
        self.addTab(self.tabFormGenVPerf, 'Verification and Performance Testing')
        self.addTab(self.tabFormReports, 'Reports')
        self.addTab(self.tabFormRunSim, 'Run Simulation')
        self.addTab(self.tabFormSimPlots, 'Simulation Plots')
        self.addTab(self.tabFormRunRpt, 'Movie ')
        self.addTab(self.tabFormGenData, 'Solution Suite')
        self.addTab(self.tabFormSetup, 'Setup')

        ## Call set form to 
        self.tabFormWelcome.Create()
        self.tabFormSetup.Create(FPIBGBase)
        self.tabFormGenConfig.Create(FPIBGBase)
        self.tabFormReports.Create(FPIBGBase)
        self.tabFormRunRpt.Create()
        self.tabFormRunSim.Create(FPIBGBase)
        self.tabFormGenData.Create(FPIBGBase)
        self.tabFormGenVPerf.Create(FPIBGBase)
        self.tabFormSimPlots.Create(FPIBGBase)
        
