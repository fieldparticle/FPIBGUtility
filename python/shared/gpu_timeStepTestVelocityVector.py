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
import pyqtgraph as pg
from random import randint
from gpu_studyVelocityVector import *
from gpu_particle import *


#################- timeStep---------------------       
def timeStepTestVelocityVector(self):
    

    if self.ps.rptFrame == True:
        print("Frame:",self.ps.frameNum)

    if self.ps.frameNum == self.ps.getEndFrame():
        self.timer.stop()
        self.ps.frameNum = 0
        self.ps.reset()
        return 
    
    self.update()

    self.plot_graph.setXRange(1, 2)
    self.plot_graph.setYRange(1, 2)
    self.plot.setAspectLocked(False)

    count = 0
    
    for ii in self.ps:
        if ii.pnum != 0:
            if(ii.colFlg == True):
                self.collisonLED.changeColor("green")
            else:
                self.collisonLED.changeColor("red")

            # Clear plot
            if count == 0:
                self.plot_graph.plot(clear = True )

            self.plot_particle(ii)
            self.plot_velocityVector(ii)
            self.plot_orientationVector(ii)
            self.plot_ProximityVector(ii)
            
            ii.colFlg = False
            #self.timer.stop()
            count +=1    
    self.ps.frameNum += 1       

def plot_line(self,x, y, pen):
    self.plot_graph.plot(
        x,
        y,
        pen=pen
    )
