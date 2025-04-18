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
from pyqtLED import QtLed

class TabRunSim(QTabWidget):

   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tcpc = TCPIPClient("TCPIP Client")
        self.tcps = TCPIPServer("TCPIP Server")
                         
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
        #self.terminal.append( Txt)

    def greenText(self,msg) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:green;\" >"
        Txt += msg
        Txt += "</span>"
        #self.terminal.append( Txt)      

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)
        
    ### Open server to recieve image files
    def openImageServerThread(self,tcps):
        if(tcps.Open() == 0):
            self.greenText( self.tcps.Text)
        else:
            self.redText( self.tcps.Text)  
        tcps.Accept()
        while tcps.RecieveBMPFile() == 0:
            self.greenText( self.tcps.Text)
            self.tcps.im = self.tcps.im.convert("RGBA")
            data = self.tcps.im.tobytes("raw","RGBA")
            qim = QImage(data, self.tcps.im.size[0], self.tcps.im.size[1],QImage.Format.Format_ARGB32)
            pix = QPixmap.fromImage(qim)
            self.image.setPixmap(pix)   
            self.command = "next"
            self.Write()
     
    def OpenImageServer(self):
        self.thread = threading.Thread(target=self.openImageServerThread,args=(self.tcps,))
        self.thread.start()

    def runSimThread(self,tcpc):
        if(tcpc.Open() == 0):
            self.greenText( self.tcpc.Text)
        else:
            self.redText( self.tcpc.Text)  
        command = "runsim"
        ret = tcpc.WriteCmd(command)
        ret = 0
        while ret == 0:
            ret = tcpc.ReadBlk(1024)
            msg = self.tcpc.Text.split(",")
            match msg[0]:
                case "perfline":
                    self.np.setText(msg[4])
                    self.fps.setText(msg[3])
                    self.spf.setText(msg[2])
                case "simdone":
                    break

            if(self.stopFlag == True):
                self.tcpc.command = "stop"
            else:
                self.tcpc.command = "cont"
            self.stopFlag = False    

            if(self.tsRunFlag == True):    
                self.tcpc.command = "tgrun"
                self.tsRunFlag = False

            if(self.changeColorFlag == True):
                if(self.row == 0):
                    self.tcpc.command = "colorc"
                if(self.row == 1):
                    self.tcpc.command = "colorang"
                self.changeColorFlag = False
            self.tcpc.Write()  
        print("Perf Study done.") 
        tcpc.Close()
        return
    def runSim(self):
        #self.simthread = threading.Thread(target=self.runSimThread,args=(self.tcpc,))
        #self.simthread.start()
        self.OpenImageServer()
       
    def stopSim(self):
        self.stopFlag = True

    def tsRun(self):
        self.tsRunFlag = True

    def changeColor(self):
        self.row = self.typlist.currentRow()
        match(self.row):
            case 0:
                self.changeColorFlag = True
            case 1:    
                self.changeColorFlag = True
            case 2:
                self.changeColorFlag = False
            case 3:                
                self.changeColorFlag = False
        
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
        tab_layout.addWidget(ctrlGrp,0,2,1,1,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)        
        ctrlgrid = QGridLayout()
        ctrlGrp.setLayout(ctrlgrid)

        self.runButton = QPushButton("Run Simulation")
        self.setSize(self.runButton,30,150)
        self.runButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.runButton,0,1,1,1)
        self.runButton.clicked.connect(self.runSim)

        self.tsButton = QPushButton("Toggle Run")
        self.setSize(self.tsButton,30,150)
        self.tsButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.tsButton,3,1,1,1)
        self.tsButton.clicked.connect(self.tsRun)
        self.tsRunFlag = False

        self.stopButton = QPushButton("Stop")
        self.setSize(self.stopButton,30,150)
        self.stopButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.stopButton,4,1,1,1)
        self.stopButton.clicked.connect(self.stopSim)
        self.stopFlag = False

        ## -------------------------------------------------------------
        ## Image Interface
        imgmgrp = QGroupBox("Image Interface")
        self.setSize(imgmgrp,500,570)
        tab_layout.addWidget(imgmgrp,1,0,1,1)
        
        paramlo = QGridLayout()
        imgmgrp.setLayout(paramlo)

        self.image = QLabel('Text')
        self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,400,545)
        paramlo.addWidget(self.image,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        #self.changeImage()

        ## -------------------------------------------------------------
        ## Mode Panel
        colorGrp = QGroupBox("Colorization")
        self.setSize(colorGrp,150,200)
        tab_layout.addWidget(colorGrp,1,2,1,1,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
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
        self.typlist.itemClicked.connect(self.changeColor)
        ColorGrid.addWidget(self.typlist)
        self.changeColorFlag = False
        

        ## -------------------------------------------------------------
        ## Performance output
        chcksgrp = QGroupBox("Performance")
        chcksgrp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        chcksgrp.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSize(chcksgrp,120,300)
        tab_layout.addWidget(chcksgrp,2,2,1,1,alignment= Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
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

        if(self.tcps.Create(FPIBBase) == 0):
            self.greenText( self.tcps.Text)
        else:
            self.redText( self.tcps.Text)  
        self.tcpc.Create(FPIBBase)
        

