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

class TabRunSim(QTabWidget):

    UpdateGUI = QtCore.pyqtSignal(object)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tcpc = TCPIPClient("TCPIP Client")
        self.tcps = TCPIPServer("TCPIP Server")
    

        

    # Deleting (Calling destructor)
    def __del__(self):
        print('Destructor called, Employee deleted.')
        self.tcpc.Close();
        self.tcps.Close();
        

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
    def startStopImage(self):
        if(self.ssImage == True):
            self.ImagestopButton.setText("Stop Image Capture")
            self.ssImage = False
            self.imageRunning = 1
            self.bmpdata_ready.connect(self.on_bmpdata_ready)
            self.bmp_image_ready.connect(self.on_bmp_image_ready)
            self.thread = threading.Thread(target=self.openImageServerThread,args=(self.tcps,))
            self.thread.start()
            return

        if(self.ssImage == False):
            self.ImagestopButton.setText("Start Image Capture")
            self.ssImage = True
            self.imageRunning = 3
            return    


    ### Open server to recieve image files
    def openImageServerThread(self,tcps):
        if(tcps.Open() == 0):
            text = self.greenText(self.tcps.Text)
            self.bmpdata_ready.emit(1,text)
        else:
            text = self.redText(self.tcps.Text)  
            self.bmpdata_ready.emit(1,text)
        tcps.Accept()
        text = self.greenText("Accepted Capture App Client")
        self.bmpdata_ready.emit(1,text)
            
        while tcps.RecieveBMPFile() == 0:
            text = self.greenText( self.tcps.Text)
            self.bmpdata_ready.emit(1,text)
            self.tcps.im = self.tcps.im.convert("RGBA")
            data = self.tcps.im.tobytes("raw","RGBA")
            qim = QImage(data, self.tcps.im.size[0], self.tcps.im.size[1],QImage.Format.Format_ARGB32)
            pix = QPixmap.fromImage(qim)
            self.bmp_image_ready.emit(pix)
            self.tcps.command = "next"
            if(self.imageRunning == 3):
                self.tcpc.command = "stopcap"
                self.imageRunning = 0
                self.tcps.Write()
                print("Closing FPIBG app Server")
                self.tcps.Close()
                break
            self.tcps.Write()        
            
                
    def OpenImageServer(self):
        self.bmpthread = threading.Thread(target=self.openImageServerThread,args=(self.tcps,))
       
        self.bmpthread.start()

    bmpdata_ready = QtCore.pyqtSignal(object,object)
    def on_bmpdata_ready(self, widget, data):
        self.terminal.append(data)

    bmp_image_ready = QtCore.pyqtSignal(object)
    def on_bmp_image_ready(self, image):
          self.image.setPixmap(image)   

    def runSimThread(self,tcpc):
        if(tcpc.Open() == 0):
            self.greenText(self.tcpc.Text)
        else:
            self.redText( self.tcpc.Text)  
        command = "runsim"
        ret = tcpc.WriteCmd(command)
        ret = 0
        while ret == 0:
            ret = tcpc.Read()
            text = self.greenText(self.tcpc.Text);
            self.data_ready.emit(1,text)
            msg = self.tcpc.Text.split(",")
            match msg[0]:
                case "perfline":
                    self.data_ready.emit(4,msg[4])
                    self.data_ready.emit(3,msg[3])
                    self.data_ready.emit(2,msg[2])
                case "simdone":
                    print("simdone")
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

            if(self.imageRunning == 1):
                self.tcpc.command = "startcap"
                self.imageRunning = 2

           

            
            self.tcpc.Write()  
            

        print("Perf Study done.") 
        tcpc.Close()
        return
    def runSim(self):
        self.simthread = threading.Thread(target=self.runSimThread,args=(self.tcpc,))
        self.data_ready.connect(self.on_data_ready)
        self.simthread.start()
        
    data_ready = QtCore.pyqtSignal(object,object)
    def on_data_ready(self, widget, data):
        match widget:
            case 4:
                self.np.setText(data)
            case 3:
                self.fps.setText(data)
            case 2:
                self.spf.setText(data)
            case 1:
                self.terminal.append(data)
            

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
        tab_layout.addWidget(ctrlGrp,0,3,1,1,alignment= Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)        
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

        self.stopButton = QPushButton("Stop Simultion")
        self.setSize(self.stopButton,30,150)
        self.stopButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.stopButton,4,1,1,1)
        self.stopButton.clicked.connect(self.stopSim)
        self.stopFlag = False

        self.ImagestopButton = QPushButton("Start Image Capure")
        self.setSize(self.ImagestopButton,30,150)
        self.ImagestopButton.setStyleSheet("background-color:  #dddddd")
        ctrlgrid.addWidget(self.ImagestopButton,5,1,1,1)
        self.ImagestopButton.clicked.connect(self.startStopImage)
        self.ssImage = True

        ## -------------------------------------------------------------
        ## Image Interface
        imgmgrp = QGroupBox("Image Interface")
        self.setSize(imgmgrp,500,570)
        tab_layout.addWidget(imgmgrp,1,0,2,2)
        
        paramlo = QGridLayout()
        imgmgrp.setLayout(paramlo)

        self.image = QLabel()
        self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,400,545)
        paramlo.addWidget(self.image,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        #self.changeImage()

        ## -------------------------------------------------------------
        ## Mode Panel
        colorGrp = QGroupBox("Colorization")
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
        self.typlist.itemClicked.connect(self.changeColor)
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

        if(self.tcps.Create(FPIBBase) == 0):
            self.greenText( self.tcps.Text)
        else:
            self.redText( self.tcps.Text)  
        self.tcpc.Create(FPIBBase)
        

