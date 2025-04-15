import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt

class TabGenData(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self,FPIBGBase):
       self.bobj = FPIBGBase
       self.cfg = self.bobj.cfg.config
       self.log = self.bobj.log.log