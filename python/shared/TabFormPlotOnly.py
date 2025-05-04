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
        self.frame = 0        
        self.fig   = pg.PlotWidget().plotItem    

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)


    def Create(self,FPIBGBase):
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.ps = GPUStudies()
        self.ps.Create()
        
        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)

        ## Image Interface
        imgmgrp = QGroupBox("Image Interface")
        #self.setSize(imgmgrp,500,570)
        tab_layout.addWidget(imgmgrp,1,0,2,2)
        
        paramlo = QGridLayout()
        imgmgrp.setLayout(paramlo)
        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0))
        self.plot_graph.setTitle("Particle Motion", color="b", size="1pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "Temperature (°C)", **styles)
        self.plot_graph.setLabel("bottom", "Time (min)", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(0.0, 3.0)
        self.plot_graph.setXRange(0.0, 3.0)
 
        paramlo.addWidget(self.plot_graph,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
           ## Control Box
        ctrlGrp = QGroupBox("Run Control")
        ctrlGrp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ctrlGrp.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSize(ctrlGrp,150,200)
        tab_layout.addWidget(ctrlGrp,0,3,1,1,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)        
        ctrlgrid = QGridLayout()
        ctrlGrp.setLayout(ctrlgrid)

        self.runButton = QPushButton("Run Simulation")
        self.setSize(self.runButton,30,150)
        self.runButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.runButton,0,1,1,1)
        #self.runButton.clicked.connect(self.startSim)
        self.runButton.clicked.connect(self.start)


    def start(self):
        # Add a timer to simulate new temperature measurements
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.frame += 1
        if self.frame == self.ps.getEndFrame():
            self.timer.stop()
            self.frame = 0
            return 
        print("plotting")

        self.ps.update()
        self.fig.clear()
        for ii in self.ps:
            r = ii.PosLoc[3]
            angle = np.linspace( 0 , 2 * np.pi , 150 ) 
            x = ii.PosLoc[0] + r * np.cos( angle ) 
            y = ii.PosLoc[1] + r * np.sin( angle ) 
            self.line = self.plot_graph
            
            if ii.pnum == 1:
                # Get a line reference
                
                self.fig = self.line.plot(
                x,
                y,
                pen='r',
                clear=True
                )
                
            else:
                # Get a line reference
                self.fig = self.line.plot(
                x,
                y,
                pen='b'
                )
            
            #self.line.setData(self.x, self.y)
        
    
       


      


   