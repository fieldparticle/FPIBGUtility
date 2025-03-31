import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from TabClass import *

import inspect
## The main window object that contains the tabs for the utility
class FPIBGMainWin(QWidget):
    def __init__(self, ObjName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ObjName = ObjName
        self.setWindowTitle('FPIBG Utility Main Window')
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon("Logo.png"))
        
        main_layout = QGridLayout(self)
        

        ## Create a tab widget
        self.tabSetup = TabObj(self)
        

        main_layout.addWidget(self.tabSetup, 0, 0, 2, 1)
        main_layout.addWidget(self.tabSetup, 0, 0, 2, 1)
        self.quitBtn = QPushButton('Quit')
        main_layout.addWidget(self.quitBtn, 2, 0,
                              alignment=Qt.AlignmentFlag.AlignRight)
        self.quitBtn.clicked.connect(self.on_clicked)
        self.setLayout(main_layout)
        self.show()

    

    def on_clicked(self) :
        exit()
        
    def Create(self,FPIBGBase):
        self.tabSetup.Create(FPIBGBase)
        self.bs = FPIBGBase
        self.bs.log.log(    1,
                            inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            0,
                            "Test 1 Main Window Success")

   