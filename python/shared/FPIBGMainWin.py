import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt
from TabClass import *
import inspect

class FPIBGMainWin(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt QTabWidget')

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        # create a tab widget
        tabSetup        = TabObj(self)
        
        # add pane to the tab widget
        tabSetup.SetForm()
        #tab.addTab(contact_page, 'Contact Info')

        main_layout.addWidget(tabSetup, 0, 0, 2, 1)
        main_layout.addWidget(tabSetup, 0, 0, 2, 1)
        main_layout.addWidget(QPushButton('Save'), 2, 0,
                              alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(QPushButton('Cancel'), 2, 0,
                              alignment=Qt.AlignmentFlag.AlignRight)

        self.show()

    def Create(self,FPIBGBase):
        self.bs = FPIBGBase
        self.bs.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            0,
                            "Created FPIBGMainWindow")

   