import sys

from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit
from PyQt6.QtWidgets import QDateEdit, QPushButton,QLabel, QGroupBox,QVBoxLayout,QHBoxLayout, QTextEdit
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
class Worker(QObject):
    progress = Signal(int)
    completed = Signal(int)
    def __init__(self, clientObj):
        QObject.__init__(self)
        self.clientObj = clientObj
    
    @Slot(int)
    def do_work(self, n):
        i = self.clientObj.tcpc.OpenAdd(self.clientObj.server_ip,self.clientObj.server_port)
       # self.progress.emit(i)
        self.completed.emit(0)

class WorkerServerOpen(QObject):
    progress = Signal(int)
    completed = Signal(int)
    def __init__(self, clientObj):
        QObject.__init__(self)
        self.clientObj = clientObj
        print("sthread")
    @Slot(int)
    def do_work(self, n):
        print("sthreadwork")
        self.greenText( self.tcps.Text)
        i = self.clientObj.tcps.Open()
        if(i == 0):
            self.greenText( self.tcps.Text)
        else:
            self.redText( self.tcps.Text)  
        self.progress.emit(i)
        self.completed.emit(0)

class WorkerServer(QObject):
    progress = Signal(int)
    completed = Signal(int)
    def __init__(self, clientObj):
        QObject.__init__(self)
        self.clientObj = clientObj
    @Slot(int)
    def do_work(self, n):
        i = self.clientObj.tcps.OpenAdd(self.clientObj.server_ip,self.clientObj.server_port)
       # self.progress.emit(i)
        self.completed.emit(0)


class WorkerRunSeries(QObject):
    progress = Signal(int)
    completed = Signal(int)
    def __init__(self, clientObj):
        QObject.__init__(self)
        self.clientObj = clientObj
    @Slot(int)
    def do_work(self, n):
        command = "runseries"
        ret = self.clientObj.tcpc.WriteCmd(command)
        self.progress.emit(ret)
        ret = 0
        while ret == 0:
            print("read")
            ret = self.clientObj.tcpc.ReadBlk(1024)
            self.progress.emit(0)
            if "perfdone" in self.clientObj.tcpc.Text:
                print()
                self.completed.emit(0)
        

class TabSetup(QTabWidget):

    print_lock = threading.Lock()
    servopenworker_requested = Signal(int)
    work_requested = Signal(int)
    work_requestedr = Signal(int)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tcpc = TCPIPClient("TCPIP Client")
        self.tcps = TCPIPServer("TCPIP Server")

    ### Threads       
    def openThread(self,tcps):
        print("Treadin")
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
       

    
    def OpenServer(self):
        #self.tcps.Open()
        self.thread = threading.Thread(target=self.openThread,args=(self.tcps,))
        self.thread.start()
        #self.thread.join()

   

    def GetImages(self):
        self.thread = threading.Thread(target=self.getImg,args=(self.tcps,))
        self.thread.start()
    

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

    def complete(self, v):
        #self.btn_start.setEnabled(True)
        self.greenText( self.tcpc.getText())
        pass
    
    def complete_open_process(self):
        self.greenText( self.tcps.getText())
    

    def completer(self, v):
        #self.btn_start.setEnabled(True)
        self.openButton.setEnabled(False)
        self.seriesButton.setEnabled(True)
        self.sseriesButton.setEnabled(True)
        self.sopenButton.setEnabled(True)
        self.greenText( "Series run was successful.")
        pass


    def update_progress(self, v):
        if(v == 0):
            self.greenText( self.tcpc.getText())
        else:
            self.redText( self.tcpc.getText())  
    #Start open server
    def starts(self):
        self.servopenworker_thread.start()
        self.work_requestedr.emit(1)
       

    #Start runseries
    def startr(self):
        self.seriesButton.setEnabled(False)
        self.sseriesButton.setEnabled(False)
        self.sopenButton.setEnabled(False)
        self.worker_threadr.start(0)
        #self.btn_start.setEnabled(False)
        n = 0
        self.work_requestedr.emit(n)
  
    #Start open client
    def start(self):
        self.openButton.setEnabled(False)
        self.worker_thread.start()
        print("Threadstart")
        #self.btn_start.setEnabled(False)
        n = 0
        self.work_requested.emit(n)
  
            

    
    def OpenClient(self):
       self.start()

    def runSeries(self):
       self.startr()

    def xmitCommand(self):
        cmd = self.command.text()
        match cmd:
            case "":
                return
            case "test":      
                self.tcpc.WriteGUI(cmd,self.terminal)
                self.tcpc.ReadGUI(self.terminal)    
            case "quit":      
                self.tcpc.CloseGUI(self.terminal)
            case "sndcsv":      
                self.tcpc.WriteGUI(cmd,self.terminal)
                self.tcpc.RecieveCSVFileGUI(self.terminal)
            case "runseries":      
                self.runSeries()
            case _:
                Text =  f"Command: " + cmd + " bad command or input" 
                self.redText(Text)
        
        self.command.setText("")
            
        
    def changeImage(self):
        pixmap = QPixmap('Logo.png')
        pixmap = pixmap.scaledToHeight(370)
        pixmap = pixmap.scaledToWidth(400)
        self.image.setPixmap(pixmap)

    def Close(self):
        self.tcpc.Close()

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)
        
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
        ## Client communctions panel
        paramgrp = QGroupBox("Client Communications")
        self.setSize(paramgrp,180,350)
        tab_layout.addWidget(paramgrp,0,0,1,2)
        
        paramlo = QGridLayout()
        paramgrp.setLayout(paramlo)

        self.ipEdit =  QLineEdit()
        self.ipEdit.setStyleSheet("background-color:  #ffffff")
        self.ipEdit.setText(self.server_ip)
        self.portEdit =  QLineEdit()
        self.portEdit.setStyleSheet("background-color:  #ffffff")
        self.portEdit.setText(str(self.server_port))

        self.openButton = QPushButton("Open Client")
        self.setSize(self.openButton,30,100)
        self.openButton.setStyleSheet("background-color:  #dddddd")
        self.openButton.clicked.connect(self.OpenClient)

        self.seriesButton = QPushButton("RunSeries")
        self.setSize(self.seriesButton,30,100)
        self.seriesButton.setStyleSheet("background-color:  #dddddd")
        self.seriesButton.clicked.connect(self.runSeries)

        paramlo.addWidget(self.portEdit,1,1)
        paramlo.addWidget(self.ipEdit,0,1)
        paramlo.addWidget(QLabel('Remote IP address'),0,0)
        paramlo.addWidget(QLabel('Remote Port'),1,0)
        paramlo.addWidget(self.openButton,2,0)
        paramlo.addWidget(self.seriesButton,2,1)


        ## -------------------------------------------------------------
        # Server communicatins parameters     
        sparamgrp = QGroupBox("Server Communications")
        self.setSize(sparamgrp,180,350)
        tab_layout.addWidget(sparamgrp,0,2,1,1)
        
        sparamlo = QGridLayout()
        sparamgrp.setLayout(sparamlo)

        self.sipLabel = QLabel('Remote IP address')
        self.setSize(self.sipLabel,30,100) 
        
        self.sipEdit =  QLineEdit()
        self.sipEdit.setStyleSheet("background-color:  #ffffff")
        self.sipEdit.setText(self.server_ip)

        self.sportLabel = QLabel('Remote Port')
        self.setSize(self.sportLabel,30,100) 
        self.sportEdit =  QLineEdit()
        self.sportEdit.setStyleSheet("background-color:  #ffffff")
        self.sportEdit.setText(str(self.server_port))

        self.sopenButton = QPushButton("Open Server")
        self.setSize(self.sopenButton,30,100)
        self.sopenButton.setStyleSheet("background-color:  #dddddd")
        self.sopenButton.clicked.connect(self.OpenServer)

        #self.sseriesButton = QPushButton("Get Image")
        #self.setSize(self.sseriesButton,30,100)
        #self.sseriesButton.setStyleSheet("background-color:  #dddddd")
        #self.sseriesButton.clicked.connect(self.GetImages)

        
        sparamlo.addWidget(self.sipEdit,0,1)
        sparamlo.addWidget(self.sipLabel,0,0)
        sparamlo.addWidget(self.sportEdit,1,2)
        sparamlo.addWidget(self.sportLabel,1,0)
        sparamlo.addWidget(self.sopenButton,2,0)
        #sparamlo.addWidget(self.sseriesButton,2,1)


        ## -------------------------------------------------------------
        ## Comunications Interface
        commgrp = QGroupBox("Communications Terminal")
        self.setSize(commgrp,450,420)
        tab_layout.addWidget(commgrp,1,0,1,2)

        commlo = QGridLayout()
        commgrp.setLayout(commlo)

        self.terminal =  QTextEdit()
        self.terminal.setStyleSheet("background-color:  #ffffff; color: green")
        self.setSize(commgrp,350,400)
        self.terminal.setAlignment(Qt.AlignmentFlag.AlignTop)
   
        self.command =  QLineEdit()
        self.command.setStyleSheet("background-color:  #ffffff")
       

        commlo.addWidget(QLabel('Terminal'),0,0)
        commlo.addWidget(self.terminal,1,0)
        commlo.addWidget(QLabel('Command'),2,0)
        commlo.addWidget(self.command,3,0)

        self.command.editingFinished.connect(self.xmitCommand)


        ## -------------------------------------------------------------
        ## Image Interface
        imgmgrp = QGroupBox("Image Interface")
        self.setSize(imgmgrp,450,420)
        tab_layout.addWidget(imgmgrp,1,2,1,2)
        
        paramlo = QGridLayout()
        imgmgrp.setLayout(paramlo)

        self.image = QLabel('Text')
        self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,370,400)
        paramlo.addWidget(self.image)
        self.changeImage()
        ##------------- Threads
        
        self.worker = Worker(self)
        self.worker_thread = QThread()
        self.worker.progress.connect(self.update_progress)
        self.worker.completed.connect(self.complete)
        self.work_requested.connect(self.worker.do_work)
        self.worker.moveToThread(self.worker_thread)
       
        
        self.workerr = WorkerRunSeries(self)
        self.worker_threadr = QThread()
        self.workerr.progress.connect(self.update_progress)
        self.workerr.completed.connect(self.completer)
        self.work_requestedr.connect(self.workerr.do_work)
        self.workerr.moveToThread(self.worker_threadr)
        
        self.servopenworker = WorkerServerOpen(self)
        self.servopenworker_thread = QThread()
        self.servopenworker.progress.connect(self.update_progress)
        self.servopenworker.completed.connect(self.complete_open_process)
        self.servopenworker_requested.connect(self.servopenworker.do_work)
        self.servopenworker.moveToThread(self.servopenworker_thread)


        if(self.tcps.Create(FPIBBase) == 0):
            self.greenText( self.tcps.Text)
        else:
            self.redText( self.tcps.Text)  
        self.tcpc.CreateGUI(FPIBBase,self.terminal)
        

   
 