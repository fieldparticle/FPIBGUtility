import sys
import importlib
from contextlib import redirect_stdout
from io import StringIO
from sys import stderr, stdout
from PyQt6.QtWidgets import QFileDialog, QGroupBox,QMessageBox
from PyQt6.QtWidgets import QGridLayout, QTabWidget, QLineEdit,QListWidget
from PyQt6.QtWidgets import QPushButton, QGroupBox
from PyQt6 import QtCore
from FPIBGConfig import FPIBGConfig
from LatexClass import *
from CfgLabel import *
from FPIBGException import *
from LatexDataConfigurationClass import *
import glob


class TabGenData(QTabWidget):
    
    texFolder = ""
    CfgFile = ""
    texFileName = ""
    hasConfig = False
    itemcfg = FPIBGConfig("Latex Class")
    startDir = "J:/MOD/FPIBGUtility/Latex"
    startDir = "J:/FPIBGJournalStaticV2/rpt"
    startDir = "J:/FPIBGDATAPY/cfg"

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
            if self.hasConfig == True:
                self.ltxObj.clearConfigGrp()
            self.ltxObj = LatexDataConfigurationClass(self)
            self.ltxObj.setConfigGroup(self.tab_layout)
            self.ltxObj.OpenLatxCFG()
            self.hasConfig = True
            files_names = self.itemcfg.config.data_dir + "/*.bin"
            files = glob.glob(files_names)
            for ii in files:
                 self.ListObj.addItem(ii)
            self.SaveButton.setEnabled(True)
            self.GenDataButton.setEnabled(True)
            gen_class = self.load_class(f"{self.itemcfg.config.import_text}.{self.itemcfg.config.import_text}")
            self.gen_obj = None
            self.gen_obj = gen_class(self.bobj,"BaseGenClass",self.itemcfg)


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



    def gen_data(self):
        self.gen_obj.gen_data()

    def load_class(self,class_name):
        module_name, class_name = class_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    
        """
        import_str = f"from {self.itemcfg.config.import_text} import *"
        module = __import__(self.itemcfg.config.import_text)
        try:
            ret = exec(import_str)     
        except BaseException as e:
            print(f"Command {import_str} is invalid or ill formed e=:")
        gen_obj = getattr(module, "run")
        module.run()
        """
        """
        self.SaveConfigurationFile()
        previewFile = f"{self.itemcfg.config.tex_dir}/preview.tex"
        previewPdf =  f"{self.itemcfg.config.tex_dir}/preview.pdf"
        previewTex = f"{self.itemcfg.config.tex_dir}/{self.itemcfg.config.name_text}.tex"
        prviewWorkingDir = self.itemcfg.config.tex_dir
        valFile = f"{self.itemcfg.config.tex_dir}/_vals_{self.itemcfg.config.name_text}.tex"
        prvCls = LatexPreview(previewFile,previewTex,prviewWorkingDir,valFile)
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
        """

        

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
            LatexcfgFile = QGroupBox("Generate/Test Particle Data")
            self.setSize(LatexcfgFile,450,500)
            self.tab_layout.addWidget(LatexcfgFile,0,0,2,2,alignment= Qt.AlignmentFlag.AlignLeft)
            
            dirgrid = QGridLayout()
            LatexcfgFile.setLayout(dirgrid)

            self.dirEdit =  QLineEdit()
            self.dirEdit.setStyleSheet("background-color:  #ffffff")
            self.dirEdit.setText("")
            self.setSize(self.dirEdit,30,450)

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

            self.newButton = QPushButton("Plot")
            self.setSize(self.newButton,30,100)
            self.newButton.setStyleSheet("background-color:  #dddddd")
            self.newButton.clicked.connect(self.browseNewItem)
            dirgrid.addWidget(self.newButton,2,1)

            self.GenDataButton = QPushButton("GenData")
            self.setSize(self.GenDataButton,30,100)
            self.GenDataButton.setStyleSheet("background-color:  #dddddd")
            self.GenDataButton.clicked.connect(self.gen_data)
            self.GenDataButton.setEnabled(False)
            dirgrid.addWidget(self.GenDataButton,2,2)

            
            self.ListObj =  QListWidget()
            #self.ListObj.setFont(self.font)
            self.ListObj.setStyleSheet("background-color:  #FFFFFF")
            self.setSize(self.ListObj,350,450)
            self.vcnt = 0            
            #self.ListObj.itemSelectionChanged.connect(lambda: self.valueChangeArray(self.ListObj))
            dirgrid.addWidget(self.ListObj,3,0,1,2)
            self.log.logs(self,"TabFormLatex finished Create.")
            
            ## -------------------------------------------------------------
            ## Comunications Interface
            self.terminal =  QTextEdit(self)
            self.terminal.setStyleSheet("background-color:  #ffffff; color: green")
            self.setSize(self.terminal,225,900)
            self.tab_layout.addWidget(self.terminal,4,0,3,3,alignment= Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        except BaseException as e:
            print(e)
   
    def valueChangeArray(self,listObj):  
        selected_items = listObj.selectedItems()
        if selected_items:
            #print("List object Value Changed",selected_items[0].text())
            self.ltxObj.setTypeText(selected_items[0].text())         
    