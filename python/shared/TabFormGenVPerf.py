import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit,QListWidget
from PyQt6.QtWidgets import QDateEdit, QPushButton,QLabel, QGroupBox,QVBoxLayout,QHBoxLayout, QTextEdit,QRadioButton,QFileDialog
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtGui import QPixmap,QImage
from PIL import Image,ImageFile
from FPIBGclient import *
from FPIBGServer import *
from _thread import *
from PIL.ImageQt import ImageQt
import threading
from io import BytesIO
ImageFile.LOAD_TRUNCATED_IMAGES = True

class TabGenVPerf(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folderLineEdit.setText(folder)
            self.log_action("browseFolder", folder)
    
    def Create(self,FPIBBase):
        self.bobj = FPIBBase;
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.server_ip = self.cfg.server_ip
        self.server_port = self.cfg.server_port
        self.client_ip = self.cfg.client_ip
        self.client_port = self.cfg.client_port

        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)

        ## -------------------------------------------------------------
        ## Mode Panel
        modegrp = QGroupBox("Mode")
        self.setSize(modegrp,120,200)
        tab_layout.addWidget(modegrp,0,0,1,2)
        
        modegrid = QGridLayout()
        modegrp.setLayout(modegrid)

        self.VerifyRadio = QRadioButton("Verify (D)",self)
        self.PerformanceRadio = QRadioButton("Performance (R)",self)
        
        modegrid.addWidget(self.VerifyRadio,1,1)
        modegrid.addWidget(self.PerformanceRadio,0,1)
        
        ## -------------------------------------------------------------
        ## Mode Panel
        typegrp = QGroupBox("Test Type")
        self.setSize(typegrp,120,150)
        tab_layout.addWidget(typegrp,0,1,1,2)
        
        typegrid = QGridLayout()
        typegrp.setLayout(typegrid)

        self.typlist = QListWidget()
        self.typlist.setStyleSheet("background-color:  #ffffff")
        self.typlist.insertItem(0, "PQB")
        self.typlist.insertItem(1, "PCD")
        self.typlist.insertItem(2, "CFB")
        self.typlist.insertItem(3, "DUP")
        typegrid.addWidget(self.typlist)
        
        ## -------------------------------------------------------------
        ## Set parent directory
        typegrp = QGroupBox("Test Parent Directory")
        self.setSize(typegrp,120,300)
        tab_layout.addWidget(typegrp,0,2,1,2)
        
        dirgrid = QGridLayout()
        typegrp.setLayout(dirgrid)

        self.dirEdit =  QLineEdit()
        self.dirEdit.setStyleSheet("background-color:  #ffffff")
        self.dirEdit.setText(self.server_ip)

        self.dirButton = QPushButton("Browse")
        self.setSize(self.dirButton,30,100)
        self.dirButton.setStyleSheet("background-color:  #dddddd")
        self.dirButton.clicked.connect(self.browseFolder)
        dirgrid.addWidget(self.dirButton,0,0)
        dirgrid.addWidget(self.dirEdit,0,1)
        