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
from gpu_studies import *
from gpu_particle import *


#################- timeStep---------------------       
def timeStep(self):
    if self.ps.rptFrame == True:
        print("Frame:",self.ps.frameNum)

    if self.ps.frameNum == self.ps.getEndFrame():
        self.timer.stop()
        self.ps.frameNum = 0
        self.ps.reset()
        return 
    
    self.ps.update()

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

            r = ii.PosLoc[3]
            angle = np.linspace( 0 , 2 * np.pi , 150 )
            x = ii.PosLoc[0] + r * np.cos( angle ) 
            y = ii.PosLoc[1] + r * np.sin( angle ) 

            if count == 0:
                self.plot_graph.plot(clear = True )
            pltpart = pg.PlotDataItem(x,y,pen=pg.mkPen(color=ii.color,width=1), brush='k')                
                #self.plot_graph.plot(
                #x,
                #y,
                #pen=pg.mkPen(color=ii.color),
                #clear = True                
            #)
        
            self.plot_graph.addItem(pltpart)
            # Center of particles   
            centerPoints = pg.ScatterPlotItem(size=10, brush='k')
            px = [ii.PosLoc[0],ii.PosLoc[0]]
            py = [ii.PosLoc[1],ii.PosLoc[1]]
            centerPoints.addPoints(px, py)
            self.plot_graph.addItem(centerPoints)

            # Velocity Vector
            if ii.pltVelVec == True:
                x,y = ii.plotVelocityVector()
                ar = pg.PlotDataItem(x,y,pen=pg.mkPen(color='g',width=2), brush='g')
                self.plot_graph.addItem(ar)
                endPoints = pg.ScatterPlotItem(size=10, brush='g')
                endPoints.addPoints(x, y)
                endPoints.setSymbol('d')
                self.plot_graph.addItem(endPoints)

            ix = []
            iy = []
            if(ii.rptIntersectionPoints == True ):
                if ii.colFlg == True:
                    intersetcPoints = pg.ScatterPlotItem(size=5, brush='g')
                    ix.append(ii.ups_i1[0])
                    ix.append(ii.ups_i2[0])
                    iy.append(ii.ups_i1[1])
                    iy.append(ii.ups_i2[1])
                    intersetcPoints.addPoints(ix, iy)
                    self.plot_graph.addItem(intersetcPoints)


            ii.colFlg = False
            
            count +=1    
    self.ps.frameNum += 1            
    
    
def plot_line(self,x, y, pen):
    self.plot_graph.plot(
        x,
        y,
        pen=pen
    )
