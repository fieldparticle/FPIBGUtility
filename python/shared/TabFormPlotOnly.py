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

class TabPlotOnly(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fig   = pg.PlotWidget().plotItem    

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    def changedt(self):
        self.dt = float(self.fps.text())
        self.ps.dt = self.dt

    def Create(self,FPIBGBase):
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        
        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)

        #------------------------------------------------------------------------------------
        ## Particle Plot Interface
        imgmgrp = QGroupBox("Particle Motion")
        self.setSize(imgmgrp,350,650)
        tab_layout.addWidget(imgmgrp,0,2,2,2)

        paramlo = QGridLayout()
        imgmgrp.setLayout(paramlo)
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground("w")
        
        self.plot_graph.setTitle("Particle Motion", color="b", size="1pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "Momentum (°C)", **styles)
        self.plot_graph.setLabel("bottom", "meters", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(0.0, 3.0)
        self.plot_graph.setXRange(0.0, 3.0)
        self.plot_graph.plotItem.vb.setAspectLocked(True)
        paramlo.addWidget(self.plot_graph,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        #------------------------------------------------------------------------------------
        ## Particle Plot Interface
        pltgrp = QGroupBox("Momentum")
        self.setSize(pltgrp,350,650)
        tab_layout.addWidget(pltgrp,2,2,2,2)

        plotlo = QGridLayout()
        pltgrp.setLayout(plotlo)
        self.plot = pg.PlotWidget()
        self.plot.setBackground("w")
        
        self.plot.setTitle("Mometum", color="b", size="1pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot.setLabel("left", "Y", **styles)
        self.plot.setLabel("bottom", "X", **styles)
        self.plot.addLegend()
        self.plot.showGrid(x=True, y=True)
        plotlo.addWidget(self.plot,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        
## -----Per study group--------------------------------------------------------
        studygrp = QGroupBox("Status")
        self.setSize(studygrp,120,100)
        tab_layout.addWidget(studygrp,0,4,1,1,alignment= Qt.AlignmentFlag.AlignLeft)
        
        studygrid = QGridLayout()
        studygrp.setLayout(studygrid)
        self.collisonLED = QtLed("red")
        self.ProcessedGraphicsLED = QtLed("red")
        self.collisionsComputeLED = QtLed("red")
        self.collisionsGraphicsLED = QtLed("red")
        
        studygrid.addWidget(QLabel('Collision:'),0,0)
        studygrid.addWidget(self.collisonLED,0,1)
        
        studygrid.addWidget(QLabel('tbd:'),1,0)
        studygrid.addWidget(self.ProcessedGraphicsLED,1,1)

        studygrid.addWidget(QLabel('tbd:'),2,0)
        studygrid.addWidget(self.collisionsComputeLED,2,1)

        studygrid.addWidget(QLabel('tbd:'),3,0)
        studygrid.addWidget(self.collisionsGraphicsLED,3,1)


        #------------------------------------------------------------------------------------
        ## Control Box
        ctrlGrp = QGroupBox("Run Control")
        ctrlGrp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ctrlGrp.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSize(ctrlGrp,75,150)
        tab_layout.addWidget(ctrlGrp,1,4,1,1,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)        
        ctrlgrid = QGridLayout()
        ctrlGrp.setLayout(ctrlgrid)

        self.runButton = QPushButton("Run")
        self.setSize(self.runButton,30,50)
        self.runButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.runButton,0,1,1,1)
        #self.runButton.clicked.connect(self.startSim)
        self.runButton.clicked.connect(self.start)

        self.stopButton = QPushButton("Stop")
        self.setSize(self.stopButton,30,50)
        self.stopButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.stopButton,0,2,1,1)
        #self.runButton.clicked.connect(self.startSim)
        self.stopButton.clicked.connect(self.stop)

        #------------------------------------------------------------------------------------
        # ## Study panel
        studyGrp = QGroupBox("Study")
        self.setSize(studyGrp,150,300)
        tab_layout.addWidget(studyGrp,2,4,1,1,alignment= Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        
        StudyLayout = QGridLayout()
        studyGrp.setLayout(StudyLayout)

        self.typlist = QListWidget()
        self.typlist.setStyleSheet("background-color:  #ffffff")
        self.typlist.insertItem(0, "2PTHorzCollisionTestHardDiscrete")
        self.typlist.insertItem(1, "2PTHorzCollisionTestSoftDiscrete")
        self.typlist.insertItem(2, "3PTHorzCollisionTestHardDiscrete")
        self.typlist.insertItem(3, "3PTHorzCollisionTestSoftDiscrete")
        self.row = 0
        self.typlist.setCurrentRow( self.row )
        #self.typlist.itemClicked.connect(self.changeColor)
        StudyLayout.addWidget(self.typlist)
        self.changeColorFlag = False

## -------------------------------------------------------------
        ## Performance output
        chcksgrp = QGroupBox("Performance")
        chcksgrp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        chcksgrp.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSize(chcksgrp,120,300)
        tab_layout.addWidget(chcksgrp,3,4,1,1,alignment= Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        dirgrid = QGridLayout()
        chcksgrp.setLayout(dirgrid)
        self.fps =  QLineEdit()
        self.fps.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.fps,20,100)
        self.fps.setText("0.01")
        self.fps.editingFinished.connect(self.changedt)
        dirgrid.addWidget(QLabel('Delta Time:'),0,0)
        dirgrid.addWidget(self.fps,0,1)
        

        self.spf =  QLineEdit()
        self.spf.setStyleSheet("background-color:  #eeeeee")
        self.setSize(self.spf,20,100)
        self.spf.setText("0")
        dirgrid.addWidget(QLabel('Seconds per Frame:'),1,0)
        dirgrid.addWidget(self.spf,1,1)
        
        self.np =  QLineEdit()
        self.np.setStyleSheet("background-color:  #eeeeee")
        self.setSize(self.np,20,100)
        self.spf.setText("0")
        dirgrid.addWidget(QLabel('Number of Particles:'),2,0)
        dirgrid.addWidget(self.np,2,1)

## -----Select Study--------------------------------------------------------        
        for ii in range(len(self.typlist)):
            match(self.typlist.currentItem().text()):
                case "2PTHorzCollisionTestHardDiscrete":
                    self.ps = GPUStudies()
                    self.ps.Create()
                    print(self.ps.desc)
                    return
                case _:
                    print("Study not found.")
        
                
        self.dt = float(self.fps.text())
        self.ps.dt = self.dt

    def stop(self):
        self.timer.stop()
#################- Start---------------------         
    def start(self):
        self.ps.reset()
        # Add a timer to simulate new temperature measurements
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.ps.frameRate)
        self.timer.timeout.connect(self.timeStep)
        self.timer.start()

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
            if(ii.colFlg == True):
                self.collisonLED.changeColor("green")
                ii.colFlg = False
            else:
                self.collisonLED.changeColor("red")

            r = ii.PosLoc[3]
            angle = np.linspace( 0 , 2 * np.pi , 150 ) 
            x = ii.PosLoc[0] + r * np.cos( angle ) 
            y = ii.PosLoc[1] + r * np.sin( angle ) 
            if count == 0:
                pen = pg.mkPen(color=ii.color)
                self.plot_graph.plot(
                    x,
                    y,
                    pen=pen,
                    clear = True                
                )
            else:
                pen = pg.mkPen(color=ii.color)
                self.plot_graph.plot(
                    x,
                    y,
                    pen=pen,
                    clear = False
                )
            
            count +=1    
        self.ps.frameNum += 1            
        
        
    def plot_line(self,x, y, pen):
        self.plot_graph.plot(
            x,
            y,
            pen=pen
        )

       


      


   