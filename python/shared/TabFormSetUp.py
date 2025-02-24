import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton,QLabel
from PyQt6.QtCore import Qt

class TabSetup(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    def Create(self):

        ## Create a container for all objects
        self.setupcontainer = QWidget(self);
        ## Set up a layout object
        self.CommPanel = QGridLayout()
        ## Add the layout to the container
        self.setupcontainer.setLayout(self.CommPanel)
        ## Add items to the layout
        self.CommPanel.addWidget(QLabel('Username:'), 0, 0)
        self.CommPanel.addWidget(QLineEdit(), 0, 1)

        #self.show()
      