import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QVBoxLayout, QGroupBox, QCheckBox, QSpinBox, QMessageBox, QListWidget, QListWidgetItem, QScrollArea
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
from FPIBGConfig import *
from FPIBGLog import *
import datetime


class TabFormConfig(QTabWidget):
    """ Object for the General Configuration Tab. This contains a form which allows the user to enter the specifications they would like to use for the simulation. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self, FPIBGBase):
        """ Constructor for the TabGenConfig object, which sets up the form on the tab. """
        # Create Base member variables
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold your main layout
        scroll_widget = QWidget()
        self.main_layout = QVBoxLayout(scroll_widget)
        
        self.cfg
        