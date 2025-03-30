import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit
from PyQt6.QtWidgets import QDateEdit, QPushButton,QLabel, QGroupBox,QVBoxLayout,QHBoxLayout, QTextEdit
from PyQt6.QtCore import Qt,QRect
from PyQt6.QtGui import QPixmap
from FPIBGclient import *
class TabSetup(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tcpc = TCPIPClient("TCPIP Client")
    
    def redText(self,msg) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:red;\" >"
        Txt += msg
        Txt += "</span>"
        self.terminal.append( Txt)

    def greenText(self,MSG) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:green;\" >"
        Txt += msg
        Txt += "</span>"
        self.terminal.append( Txt)


    def Open(self):
        self.tcpc.OpenGUI(self.terminal)
        
    
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

        
    def Create(self,FPIBBase):
        self.bobj = FPIBBase;
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.server_ip = self.cfg.server_ip
        self.server_port = self.cfg.server_port
       

        self.setStyleSheet("background-color:  #eeeeee")
        tab_layout = QGridLayout()
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(tab_layout)

        ## -------------------------------------------------------------
        ## Communicastions parameters and test
        paramgrp = QGroupBox("Communications Parameters")
        paramgrp.setMinimumHeight(180)
        paramgrp.setMinimumWidth(350)
        paramgrp.setMaximumHeight(180)
        paramgrp.setMaximumWidth(350)
        tab_layout.addWidget(paramgrp,0,0)
        
        paramlo = QGridLayout()
        paramgrp.setLayout(paramlo)

        
        self.ipEdit =  QLineEdit()
        self.ipEdit.setStyleSheet("background-color:  #ffffff")
        self.ipEdit.setText(self.server_ip)
        self.portEdit =  QLineEdit()
        self.portEdit.setStyleSheet("background-color:  #ffffff")
        self.portEdit.setText(str(self.server_port))
        self.openButton = QPushButton("Open")
        self.openButton.setStyleSheet("background-color:  #dddddd")
        self.openButton.clicked.connect(self.Open)
        paramlo.addWidget(self.portEdit,1,1)
        paramlo.addWidget(self.ipEdit,0,1)
        paramlo.addWidget(QLabel('Remote IP address'),0,0)
        paramlo.addWidget(QLabel('Remote Port'),1,0)
        paramlo.addWidget(self.openButton,2,0)


        ## -------------------------------------------------------------
        ## Comunications Interface
        commgrp = QGroupBox("Communications Terminal")
        commgrp.setMinimumHeight(450)
        commgrp.setMaximumHeight(450)
        commgrp.setMinimumWidth(420)
        commgrp.setMaximumWidth(420)
        tab_layout.addWidget(commgrp,1,0)

        commlo = QGridLayout()
        commgrp.setLayout(commlo)

        self.terminal =  QTextEdit()
        self.terminal.setStyleSheet("background-color:  #ffffff; color: green")
        self.terminal.setMinimumHeight(350)
        self.terminal.setMaximumHeight(350)
        self.terminal.setMinimumWidth(400)
        self.terminal.setMaximumWidth(400)
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
        imgmgrp.setMinimumHeight(450)
        imgmgrp.setMaximumHeight(450)
        imgmgrp.setMinimumWidth(420)
        imgmgrp.setMaximumWidth(420)
        tab_layout.addWidget(imgmgrp,1,2)
        
        paramlo = QGridLayout()
        imgmgrp.setLayout(paramlo)

        self.image = QLabel('Text')
        self.image.setStyleSheet("background-color:  #ffffff")
        self.image.setMinimumHeight(370)
        self.image.setMaximumHeight(370)
        self.image.setMinimumWidth(400)
        self.image.setMaximumWidth(400)
        paramlo.addWidget(self.image)
        self.changeImage()
        self.tcpc.CreateGUI(FPIBBase,self.terminal)
        

   
 