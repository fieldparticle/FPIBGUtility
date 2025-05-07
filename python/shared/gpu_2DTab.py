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
from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from ps_ParticleSystem import *
from gpu_LockCellArray import *
from gpu_plotParticle import *
import pyqtgraph as pg
from time import sleep

class GPU2DTab(QTabWidget):

    UpdateGUI = QtCore.pyqtSignal(object)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssImage = True

        

    # Deleting (Calling destructor)
    def __del__(self):
        print('Destructor called, Employee deleted.')
        

    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folderLineEdit.setText(folder)
            self.log_action("browseFolder", folder)
    
    def redText(self,msg) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:red;\" >"
        Txt += msg
        Txt += "</span>"
        return Txt
        #self.terminal.append(Txt)

    def greenText(self,msg) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:green;\" >"
        Txt += msg
        Txt += "</span>"
        return Txt
        #self.terminal.append(Txt)      

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)
        
    imageRunning = 0
    def startSim(self):
        if(self.ssImage == True):
            self.ssImage = False
            self.imageRunning = 1
            #self.bmp_image_ready.connect(self.on_bmp_image_ready)
            self.thread = threading.Thread(target=self.openImageServerThread,args=(1,))
            self.thread.start()
            return

        if(self.ssImage == False):
            self.ssImage = True
            self.imageRunning = 3
            return    

#######################################################################################
    ### Open server to recieve image files
    def openImageServerThread(self,tcps):
        for tt in range(self.ps.endFrame):
        #print("Frame:",tt)
            for ii in range(self.ps.totParts):
                t =threading.Thread(target=self.ps.processVertex,args=(ii,))
                t.start()
                t.join()
            pixmap = self.ps.plotParts.plotParticle(self.image)
            sleep(10)
        #self.bmp_image_ready.emit(pixmap)
        #bmp_image_ready = QtCore.pyqtSignal(object)

#-----------------------------------------------------------------------------------        
    def on_bmp_image_ready(self, image):
          self.image.setPixmap(image)   
#######################################################################################
    def stopSim(self):
        self.stopFlag = True

    def tsRun(self):
        self.tsRunFlag = True

        
    def Create(self,FPIBBase):
        self.bobj = FPIBBase;
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.server_ip = self.cfg.server_ip
        self.server_port = self.cfg.server_port
        self.client_ip = self.cfg.client_ip
        self.client_port = self.cfg.client_port
        self.save_csv_dir = self.cfg.save_csv_dir
        self.testfile = self.cfg.application.testfile

        self.ps = ParticleSystem()
        self.ps.setTimeStep(0.01)

        self.ps.addParm(1.0,100,[1.0,1.5,1.5],[1.0,0.0,0.0],0.25)
        self.ps[0].setColor((0.1, 0.2, 0.5))

        self.ps.addParm(1.0,150,[2.0,1.5,1.5],[-1.0,0.0,0.0],0.25)
        self.ps[0].setColor((0.6, 0.2, 0.5))
        self.ps.setEndFrame(20)


        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)
        ## -------------------------------------------------------------
        ## Set parent directory
        typegrp = QGroupBox("Simulation File to run")
        self.setSize(typegrp,70,600)
        tab_layout.addWidget(typegrp,0,0,1,1,alignment= Qt.AlignmentFlag.AlignLeft)
        
        dirgrid = QGridLayout()
        typegrp.setLayout(dirgrid)

        self.dirEdit =  QLineEdit()
        self.dirEdit.setStyleSheet("background-color:  #ffffff")
        self.dirEdit.setText(self.testfile)

        self.dirButton = QPushButton("Browse")
        self.setSize(self.dirButton,30,100)
        self.dirButton.setStyleSheet("background-color:  #dddddd")
        self.dirButton.clicked.connect(self.browseFolder)
        dirgrid.addWidget(self.dirButton,0,0)
        dirgrid.addWidget(self.dirEdit,0,1)

         ## -------------------------------------------------------------
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
        self.runButton.clicked.connect(self.openImageServerThread)

        self.tsButton = QPushButton("Pause")
        self.setSize(self.tsButton,30,150)
        self.tsButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.tsButton,3,1,1,1)
        self.tsButton.clicked.connect(self.tsRun)
        self.tsRunFlag = False

        self.stopButton = QPushButton("Stop Simultion")
        self.setSize(self.stopButton,30,150)
        self.stopButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.stopButton,4,1,1,1)
        self.stopButton.clicked.connect(self.stopSim)
        self.stopButton.setEnabled(False)
        self.stopFlag = False

        ## -------------------------------------------------------------
        ## Image Interface
        imgmgrp = QGroupBox("Image Interface")
        self.setSize(imgmgrp,500,570)
        tab_layout.addWidget(imgmgrp,1,0,2,2)
        
        paramlo = QGridLayout()
        imgmgrp.setLayout(paramlo)
        self.image = pg.PlotWidget()
        self.image.setBackground('w')
        #self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,400,545)
        paramlo.addWidget(self.image,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        #self.changeImage()

        ## -------------------------------------------------------------
        ## Mode Panel
        colorGrp = QGroupBox("Tests")
        self.setSize(colorGrp,150,200)
        tab_layout.addWidget(colorGrp,2,3,1,1,alignment= Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        
        ColorGrid = QGridLayout()
        colorGrp.setLayout(ColorGrid)

        self.typlist = QListWidget()
        self.typlist.setStyleSheet("background-color:  #ffffff")
        self.typlist.insertItem(0, "Colllions (Red=True,Blue=False)")
        self.typlist.insertItem(1, "Velocity Angle (HSV)")
        self.typlist.insertItem(2, "Velocity Magnitude (CM)")
        self.typlist.insertItem(3, "Pressure (CM)")
        self.row = 0
        self.typlist.setCurrentRow( self.row )
        #self.typlist.itemClicked.connect(self.changeColor)
        ColorGrid.addWidget(self.typlist)
        self.changeColorFlag = False
        
        ## -------------------------------------------------------------
        ## Comunications Interface
        commgrp = QGroupBox("Communications Terminal")
        self.setSize(commgrp,225,300)
        tab_layout.addWidget(commgrp,1,3,1,1,alignment= Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        commlo = QGridLayout()
        commgrp.setLayout(commlo)

        self.terminal =  QTextEdit()
        self.terminal.setStyleSheet("background-color:  #ffffff; color: green")
        self.setSize(commgrp,225,300)
    #self.terminal.setAlignment(Qt.AlignmentFlag.AlignTop)
        commlo.addWidget(self.terminal,1,0)
   
        ## -------------------------------------------------------------
        ## Performance output
        chcksgrp = QGroupBox("Performance")
        chcksgrp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        chcksgrp.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSize(chcksgrp,120,300)
        tab_layout.addWidget(chcksgrp,3,3,1,1,alignment= Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        dirgrid = QGridLayout()
        chcksgrp.setLayout(dirgrid)
        self.fps =  QLineEdit()
        self.fps.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.fps,20,100)
        self.fps.setText("0")
        dirgrid.addWidget(QLabel('Frames per second:'),0,0)
        dirgrid.addWidget(self.fps,0,1)
        

        self.spf =  QLineEdit()
        self.spf.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.spf,20,100)
        self.spf.setText("0")
        dirgrid.addWidget(QLabel('Seconds per Frame:'),1,0)
        dirgrid.addWidget(self.spf,1,1)
        
        self.np =  QLineEdit()
        self.np.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.np,20,100)
        self.spf.setText("0")
        dirgrid.addWidget(QLabel('Number of Particles:'),2,0)
        dirgrid.addWidget(self.np,2,1)

      

