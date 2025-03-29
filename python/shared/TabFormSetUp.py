import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton,QLabel, QGroupBox,QVBoxLayout
from PyQt6.QtCore import Qt

class TabSetup(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    def Create(self):
        layout = QVBoxLayout()
        #layout.setGeometry(100,100)
        self.setLayout(layout)
        self.Label001 = QLabel('Username:')
        self.Label001.setMinimumSize(80, 20)
        
        self.edit001 =  QLineEdit()
        self.edit001.setMinimumSize(30, 20)
        self.edit001.setMaximumHeight(40)
        self.edit001.setMaximumWidth(30)
        layout.addWidget(self.Label001)
        layout.addWidget(self.edit001)
        
        
        
        ## Create a container for all objects
        #self.setupcontainer = QWidget(self)
        ## Set up a layout object
        #self.CommPanel = QGridLayout()
        ### Add the layout to the container
        #self.setupcontainer.setLayout(self.CommPanel)
        ## Add items to the layout
        #self.CommPanel.addWidget(QLabel('Username:'), 0, 0)
        #self.CommPanel.addWidget(QLineEdit(), 0, 1)

        self.show()
      