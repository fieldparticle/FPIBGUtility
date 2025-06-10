import sys
from contextlib import redirect_stdout
from io import StringIO
from sys import stderr, stdout
from PyQt6.QtWidgets import QFileDialog, QGroupBox,QMessageBox
from PyQt6.QtWidgets import QGridLayout, QTabWidget, QLineEdit,QListWidget
from PyQt6.QtWidgets import QPushButton, QGroupBox
from PyQt6 import QtCore
from FPIBGclient import *
from FPIBGServer import *
from _thread import *
from FPIBGConfig import FPIBGConfig
from LatexClass import *
from CfgLabel import *
from FPIBGException import *
from LatexSingleImage import *
from LatexMultiImage import *
from LatexPlotBase import *
from LatexPlotParticle import *
from LatexPlot import *
from LatexSingleTable import *


def p(x):
    print (x)
class EmbeddedTerminal(QTextEdit):
    def __init__(self, parent):
        super(EmbeddedTerminal, self).__init__(parent)

    def run_func(self, func, *args, **kwargs):
        self.thread = QThread()
        self.worker = TerminalWorker(func, args, kwargs)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_terminal)
        self.thread.start()

    def update_terminal(self, text):
        self.setText(text)


class TerminalWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, func, args, kwargs):
        QObject.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        with redirect_stdout(StringIO()) as f:
            self.func(*self.args, **self.kwargs)
        output = f.getvalue()
        self.progress.emit(output)

class TabFormLatex(QTabWidget):
    
    texFolder = ""
    CfgFile = ""
    texFileName = ""
    hasConfig = False
    itemcfg = FPIBGConfig("Latex Class")
    startDir = "J:/MOD/FPIBGUtility/Latex"
    startDir = "J:/FPIBGJournalStaticV2/rpt"
    startDir = "J:/FPIBGJournalStaticV2/cfg"

    ObjName = ""
    ltxObj = None

    def __init__(self, FPIBGBase, ObjName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.log.logs(self,"TabFormLatex finished init.")
        
    
    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    def SaveConfigurationFile(self):
        self.ltxObj.updateCfgData()
        
        #self.ltxObj.clearConfigGrp()

  
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        #folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        folder = QFileDialog.getOpenFileName(self, ("Open File"),
                                       self.startDir,
                                       ("Configuration File (*.cfg)"))
        
        if folder[0]:
            self.CfgFile = folder[0]
            self.texFolder = os.path.dirname(self.CfgFile)
            self.texFileName = os.path.splitext(os.path.basename(self.CfgFile))[0]
            self.dirEdit.setText(self.CfgFile)
            try :
                self.itemcfg = FPIBGConfig(self.CfgFile)
                self.itemcfg.Create(self.bobj.log,self.CfgFile)
                
            except BaseException as e:
                print(f"Unable to open item configurations file:{e}")
                self.hasConfig = False
                return 
            self.type = self.itemcfg.config.type_text 
            if self.hasConfig == True:
                self.ltxObj.clearConfigGrp()
            if "multiimage" in self.type:
                self.ltxObj = LatexMultiImage(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.ListObj.setEnabled(False)
                self.hasConfig = True
            elif "image" in self.type:
                self.ltxObj = LatexSingleImage(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.setImgGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "singletable" in self.type:
                self.ltxObj = LatexSingleTable(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "plotparticle" in self.type:
                self.ltxObj = LatexPlotParicle(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "plot" in self.type:
                self.ltxObj = LatexPlot(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            elif "type" in self.type:
                self.ltxObj = LatexSingleImage(self)
                self.ltxObj.setConfigGroup(self.tab_layout)
                self.ltxObj.setImgGroup(self.tab_layout)
                self.ltxObj.OpenLatxCFG()
                self.hasConfig = True
            else:
                print("InvalidType")
                return
            
           
            self.SaveButton.setEnabled(True)
            self.PreviewButton.setEnabled(True)


    def browseNewItem(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        #folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if(self.ListObj.currentRow() < 0):
            print("Must select type first.")
            return
        else:
            print(f"Opening Row {self.ListObj.currentRow()}")

        folder = QFileDialog.getSaveFileName(self, ("Open File"),
                                       "J:/FPIBGJournalStaticV2/rpt",
                                       ("Images (*.cfg)"))
        cfg_cnt = ""
        if folder[0]:
            self.CfgFile = folder[0]
            with open(self.cfg.single_template, 'r') as file:
                cfg_cnt = file.read()
            #print(cfg_cnt)
            file.close()
            with open(folder[0], 'w') as file:
                file.write(cfg_cnt)
                file.close()
            self.texFolder = os.path.dirname(self.CfgFile)
            self.texFileName = os.path.splitext(os.path.basename(self.CfgFile))[0]
            self.dirEdit.setText(self.CfgFile)
            self.OpenLatxCFG(self.CfgFile)
   
    def preview(self):
        self.SaveConfigurationFile()
        previewFile = f"{self.itemcfg.config.tex_dir}/preview.tex"
        previewPdf =  f"{self.itemcfg.config.tex_dir}/preview.pdf"
        previewTex = f"{self.itemcfg.config.tex_dir}/{self.itemcfg.config.name_text}.tex"
        prviewWorkingDir = self.itemcfg.config.tex_dir
        prvCls = LatexPreview(previewFile,previewTex,prviewWorkingDir,self.itemcfg.config.values_file_text)
        prvCls.ProcessLatxCode()
        prvCls.Run()
        with open('termPreview.log', "r") as infile:  
            txt_line = infile.readline().strip("\n")
            self.terminal.append(txt_line)
            while txt_line:
                txt_line = infile.readline().strip("\n")
                self.terminal.append(txt_line)
        prv = PreviewDialog(previewPdf)
        prv.exec()
        

        

    def Create(self):
        self.log.logs(self,"TabFormLatex started Create.")
        try:
            self.setStyleSheet("background-color:  #eeeeee")
            self.tab_layout = QGridLayout()
            self.tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.setLayout(self.tab_layout)

            ## -------------------------------------------------------------
            ## Set parent directory
            LatexcfgFile = QGroupBox("Latex File Configuration")
            self.setSize(LatexcfgFile,200,300)
            self.tab_layout.addWidget(LatexcfgFile,0,0,1,2,alignment= Qt.AlignmentFlag.AlignLeft)
            
            dirgrid = QGridLayout()
            LatexcfgFile.setLayout(dirgrid)

            self.dirEdit =  QLineEdit()
            self.dirEdit.setStyleSheet("background-color:  #ffffff")
            self.dirEdit.setText("")

            self.dirButton = QPushButton("Browse")
            self.setSize(self.dirButton,30,100)
            self.dirButton.setStyleSheet("background-color:  #dddddd")
            self.dirButton.clicked.connect(self.browseFolder)
            dirgrid.addWidget(self.dirButton,0,0)
            dirgrid.addWidget(self.dirEdit,0,1)

            self.SaveButton = QPushButton("Save")
            self.setSize(self.SaveButton,30,100)
            self.SaveButton.setStyleSheet("background-color:  #dddddd")
            self.SaveButton.clicked.connect(self.SaveConfigurationFile)
            self.SaveButton.setEnabled(False)
            dirgrid.addWidget(self.SaveButton,2,0)

            self.newButton = QPushButton("New")
            self.setSize(self.newButton,30,100)
            self.newButton.setStyleSheet("background-color:  #dddddd")
            self.newButton.clicked.connect(self.browseNewItem)
            dirgrid.addWidget(self.newButton,2,1)

            self.PreviewButton = QPushButton("Preview")
            self.setSize(self.PreviewButton,30,100)
            self.PreviewButton.setStyleSheet("background-color:  #dddddd")
            self.PreviewButton.clicked.connect(self.preview)
            self.PreviewButton.setEnabled(False)
            dirgrid.addWidget(self.PreviewButton,2,2)

            self.ListObj =  QListWidget()
            #self.ListObj.setFont(self.font)
            self.ListObj.setStyleSheet("background-color:  #FFFFFF")
            self.vcnt = 0            
            self.ListObj.insertItem(0, "image")
            self.ListObj.insertItem(1, "plot")
            self.ListObj.insertItem(2, "multiplot")
            self.ListObj.insertItem(3, "multiimage")
            self.ListObj.itemSelectionChanged.connect(lambda: self.valueChangeArray(self.ListObj))
            dirgrid.addWidget(self.ListObj,3,0,1,2)
            self.log.logs(self,"TabFormLatex finished Create.")

            ## -------------------------------------------------------------
            ## Comunications Interface
            self.terminal =  QTextEdit(self)
            self.terminal.setStyleSheet("background-color:  #ffffff; color: green")
            self.setSize(self.terminal,225,900)
            self.tab_layout.addWidget(self.terminal,4,0,1,3,alignment= Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        except BaseException as e:
            print(e)
   
    def valueChangeArray(self,listObj):  
        selected_items = listObj.selectedItems()
        if selected_items:
            #print("List object Value Changed",selected_items[0].text())
            self.ltxObj.setTypeText(selected_items[0].text())         
    