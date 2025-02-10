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
    
    def SetForm(self):
        # personal page
        personal_page = QWidget(self)
        layout = QFormLayout()
        personal_page.setLayout(layout)
        layout.addRow('First Name:', QLineEdit(self))
        layout.addRow('Last Name:', QLineEdit(self))
        layout.addRow('DOB:', QDateEdit(self))
        self.addTab(personal_page, 'Personal Info')

        # contact pane
        contact_page = QWidget(self)
        layout = QFormLayout()
        contact_page.setLayout(layout)
        layout.addRow('Phone Number:', QLineEdit(self))
        layout.addRow('Email Address:', QLineEdit(self))
        self.addTab(contact_page, 'Personal Info')