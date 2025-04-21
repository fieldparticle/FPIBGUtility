import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit,QListWidget
from PyQt6.QtWidgets import QDateEdit, QPushButton,QLabel, QGroupBox,QVBoxLayout,QHBoxLayout, QTextEdit,QRadioButton,QFileDialog
from PyQt6.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap,QImage
from PIL import Image,ImageFile
from FPIBGclient import *
from FPIBGServer import *
from _thread import *
from PIL.ImageQt import ImageQt
import threading
from io import BytesIO
from pyqtLED import QtLed


class TabSimPlots(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self,FPIBGBase):
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)
        tbdLabel = QLabel("To be Completed")
        tbdLabel.setStyleSheet("font: 30pt Comic Sans MS")
        vectpolt = QLabel()
        self.pixmap = QPixmap("SimpVectPlotFiltered.png")
        vectpolt.setPixmap(self.pixmap)
        tab_layout.addWidget(tbdLabel)
        tab_layout.addWidget(vectpolt)