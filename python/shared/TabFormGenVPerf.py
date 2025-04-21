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

ImageFile.LOAD_TRUNCATED_IMAGES = True

class TabGenVPerf(QTabWidget):
    
    stopFlag = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tcpc = TCPIPClient("TCPIP Client")
        self.tcps = TCPIPServer("TCPIP Server")

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.dirEdit.setText(folder)

    def redText(self,msg) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:red;\" >"
        Txt += msg
        Txt += "</span>"
        self.terminal.append( Txt)

    def greenText(self,msg) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:green;\" >"
        Txt += msg
        Txt += "</span>"
        self.terminal.append( Txt)      

    def stop(self):
        self.stopFlag = True
        
    def runSeriesThread(self,tcpc):
        if(tcpc.Open() == 0):
            self.greenText( self.tcpc.Text)
        else:
            self.redText( self.tcpc.Text)  
        command = "runseries,particleVP.cfg"
        ret = tcpc.WriteCmd(command)
        ret = 0
        while ret == 0:
            ret = tcpc.ReadBlk(1024)
            msg = self.tcpc.Text.split(",")
            match msg[0]:
                case "perfline":
                    self.loadedDisk.setText(msg[7])
                    self.processedGraphics.setText(msg[9])
                    self.processedCompute.setText(msg[8])
                    self.collisionsDisk.setText(msg[10]) 
                    self.collisionsComp.setText(msg[11])
                    if msg[14] == "1":
                        self.processedComputeLED.changeColor("red")    
                    if msg[15] == "1":
                        self.ProcessedGraphicsLED.changeColor("red")    
                    if msg[16] == "1":
                        self.collisionsComputeLED.changeColor("red") 
                case "csvfile":
                    ret = tcpc.RecieveCSVFile()        
                    self.greenText(tcpc.Text)
                case "perfdone":
                    break
            self.tcpc.command = "cont"
            if(self.stopFlag == True):
                self.tcpc.command = "stop"
                ret = 1
            self.tcpc.Write()            
        print("Perf Study done.") 
        self.greenText("Perf Study Done.")
    def runSeries(self):
        self.thread = threading.Thread(target=self.runSeriesThread,args=(self.tcpc,))
        self.thread.start()
    
    def Create(self,FPIBBase):
        self.bobj = FPIBBase;
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.server_ip = self.cfg.server_ip
        self.server_port = self.cfg.server_port
        self.client_ip = self.cfg.client_ip
        self.client_port = self.cfg.client_port
        self.save_csv_dir = self.cfg.save_csv_dir

        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
       # tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
     #   tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)

        ## -------------------------------------------------------------
        ## Mode Panel
        modegrp = QGroupBox("Mode")
        self.setSize(modegrp,120,200)
        tab_layout.addWidget(modegrp,0,0,1,2,alignment= Qt.AlignmentFlag.AlignLeft)
        
        modegrid = QGridLayout()
        modegrp.setLayout(modegrid)

        self.VerifyRadio = QRadioButton("Verify (D)",self)
        self.PerformanceRadio = QRadioButton("Performance (R)",self)
        self.PerformanceRadio.toggle()
        modegrid.addWidget(self.VerifyRadio,1,1)
        modegrid.addWidget(self.PerformanceRadio,0,1)

        
        ## -------------------------------------------------------------
        ## Mode Panel
        typegrp = QGroupBox("Test Type")
        self.setSize(typegrp,120,150)
        tab_layout.addWidget(typegrp,0,1,1,2,alignment= Qt.AlignmentFlag.AlignLeft)
        
        typegrid = QGridLayout()
        typegrp.setLayout(typegrid)

        self.typlist = QListWidget()
        self.typlist.setStyleSheet("background-color:  #ffffff")
        self.typlist.insertItem(0, "PQB")
        self.typlist.insertItem(1, "PCD")
        self.typlist.insertItem(2, "CFB")
        self.typlist.insertItem(3, "DUP")
        self.typlist.setCurrentRow(0)

        typegrid.addWidget(self.typlist)
        
        ## -------------------------------------------------------------
        ## Set parent directory
        typegrp = QGroupBox("Test Parent Directory")
        self.setSize(typegrp,120,300)
        tab_layout.addWidget(typegrp,0,2,1,2,alignment= Qt.AlignmentFlag.AlignLeft)
        
        dirgrid = QGridLayout()
        typegrp.setLayout(dirgrid)

        self.dirEdit =  QLineEdit()
        self.dirEdit.setStyleSheet("background-color:  #ffffff")
        self.dirEdit.setText(self.save_csv_dir)

        self.dirButton = QPushButton("Browse")
        self.setSize(self.dirButton,30,100)
        self.dirButton.setStyleSheet("background-color:  #dddddd")
        self.dirButton.clicked.connect(self.browseFolder)
        dirgrid.addWidget(self.dirButton,0,0)
        dirgrid.addWidget(self.dirEdit,0,1)


        ## -------------------------------------------------------------
        ## Verification Checks
        chcksgrp = QGroupBox("Verification Checks")
        self.setSize(chcksgrp,120,600)
        tab_layout.addWidget(chcksgrp,1,0,1,3,alignment= Qt.AlignmentFlag.AlignLeft)
        
        dirgrid = QGridLayout()
        chcksgrp.setLayout(dirgrid)
        
        self.loadedDisk =  QLineEdit()
        self.loadedDisk.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.loadedDisk,20,100)
        self.loadedDisk.setText("0")

        self.loadedGPU =  QLineEdit()
        self.loadedGPU.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.loadedGPU,20,100)
        self.loadedGPU.setText("0")

        self.processedCompute =  QLineEdit()
        self.processedCompute.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.processedCompute,20,100)
        self.processedCompute.setText("0")

        self.processedGraphics =  QLineEdit()
        self.processedGraphics.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.processedGraphics,20,100)
        self.processedGraphics.setText("0")

        #self.loadedDiskLED = QtLed("green")
        #self.loadedGPULED = QtLed("green")
        self.processedComputeLED = QtLed("green")
        self.ProcessedGraphicsLED = QtLed("green")
        self.collisionsComputeLED = QtLed("green")
        self.collisionsGraphicsLED = QtLed("red")

        self.collisionsDisk =  QLineEdit()
        self.collisionsDisk.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.collisionsDisk,20,100)
        self.collisionsDisk.setText("0")

        self.collisionsComp =  QLineEdit()
        self.collisionsComp.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.collisionsComp,20,100)
        self.collisionsComp.setText("0")

        dirgrid.addWidget(QLabel('Particles loaded from disk:'),0,0)
        dirgrid.addWidget(self.loadedDisk,0,1)
        # dirgrid.addWidget(self.loadedDiskLED,0,2)
        #dirgrid.addWidget(QLabel('Particles loaded to GPU:'),1,0)
        #dirgrid.addWidget(self.loadedGPU,1,1)
       #dirgrid.addWidget(self.loadedGPULED,1,2)
        dirgrid.addWidget(QLabel('Particles processed in compute:'),2,0)
        dirgrid.addWidget(self.processedCompute,2,1)
        dirgrid.addWidget(self.processedComputeLED,2,2)
        dirgrid.addWidget(QLabel('Particles processed in graphics:'),3,0)
        dirgrid.addWidget(self.processedGraphics,3,1)
        dirgrid.addWidget(self.ProcessedGraphicsLED,3,2)

        dirgrid.addWidget(QLabel('Collisions loaded from disk:'),0,4)
        dirgrid.addWidget(self.collisionsDisk,0,5)
        dirgrid.addWidget(self.collisionsComputeLED,0,6)
        dirgrid.addWidget(QLabel('Collisions Compute:'),1,4)
        dirgrid.addWidget(self.collisionsComp,1,5)
        dirgrid.addWidget(self.collisionsComputeLED,1,6)

        ## -------------------------------------------------------------
        ## Comunications Interface
        commgrp = QGroupBox("Communications Terminal")
        self.setSize(commgrp,450,420)
        tab_layout.addWidget(commgrp,2,0,1,2,alignment= Qt.AlignmentFlag.AlignLeft)

        commlo = QGridLayout()
        commgrp.setLayout(commlo)

        self.terminal =  QTextEdit()
        self.terminal.setStyleSheet("background-color:  #ffffff; color: green")
        self.setSize(commgrp,350,750)
        self.terminal.setAlignment(Qt.AlignmentFlag.AlignTop)
   
        self.command =  QLineEdit()
        self.command.setStyleSheet("background-color:  #ffffff")
       
        commlo.addWidget(QLabel('Terminal'),0,0)
        commlo.addWidget(self.terminal,1,0)
        commlo.addWidget(QLabel('Command'),2,0)
        commlo.addWidget(self.command,3,0)

       #self.command.editingFinished.connect(self.xmitCommand)
        
        ## -------------------------------------------------------------
        ## Series Box
        serGrp = QGroupBox("Series Type")
        serGrp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setSize(serGrp,100,100)
        tab_layout.addWidget(serGrp,2,3,1,1,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)        
        sergrid = QGridLayout()
        serGrp.setLayout(sergrid)


        self.seriesRadio = QRadioButton("Series",self)
        self.seriesRadio.toggle()
        #self.seriesRadio.setStyleSheet("background-color:  #ffffff")
        self.singleRadio = QRadioButton("Single",self)
        #self.singleRadio.setStyleSheet("background-color:  #ffffff")
        
        sergrid.addWidget(self.seriesRadio,1,0)
        sergrid.addWidget(self.singleRadio,0,0)

        ## -------------------------------------------------------------
        ## Control Box
        ctrlGrp = QGroupBox("Run Control")
        ctrlGrp.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setSize(ctrlGrp,100,130)
        tab_layout.addWidget(ctrlGrp,2,3,1,1,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)        
        ctrlgrid = QGridLayout()
        ctrlGrp.setLayout(ctrlgrid)

        self.runButton = QPushButton("Run Tests")
        self.setSize(self.runButton,30,100)
        self.runButton.setStyleSheet("background-color:  #dddddd")
        #self.runButton.clicked.connect(self.DoAll)
        ctrlgrid.addWidget(self.runButton,0,1,1,1)
        self.runButton.clicked.connect(self.runSeries)

        self.stopButton = QPushButton("Stop")
        self.setSize(self.stopButton,30,100)
        self.stopButton.setStyleSheet("background-color:  #dddddd")
        self.stopButton.clicked.connect(self.stop)
        ctrlgrid.addWidget(self.stopButton,1,1,1,1)

        if(self.tcps.Create(FPIBBase) == 0):
            self.greenText( self.tcps.Text)
        else:
            self.redText( self.tcps.Text)  
        self.tcpc.CreateGUI(FPIBBase,self.terminal)