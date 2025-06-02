from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QGroupBox,QMessageBox,QDialog
from CfgLabel import *
from LatexClass import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
import numpy as np
from LatexConfigurationClass import *
from LatexSinglePlot import * 

class LatexSinglePlotParicle(LatexSinglePlot):
    fignum = 0
    
    data = None
    hasPlot = False
    npdata = None
    fig = None
    ax = None
    pixmap = None
    hasRawData = False
    hasSummaryData = False
    topdir = ""
    sumFile = ""
    data_files = []
    average_list = []

    def __init__(self,Parent):
        super().__init__(Parent)
        

    def __exit__(self):
        plt.close("all")
  
    def updatePlot(self):
        if(self.fignum != 0):
            plt.close("all")
        self.fignum += 1
        self.fig = plt.figure(self.fignum)
        self.ax = self.fig.gca()
        if self.hasPlot == True:
            for oob in self.objArry:
                cmd_lst = oob.key.split('_')
                matches = ["plt","ax","fig"]
                class_major = None
                if any(x in cmd_lst[0] for x in matches):
                    match(cmd_lst[0]):
                        case "ax":
                            class_major = self.ax
                        case "plt":
                            class_major = plt
                        case "fig":
                            class_major = self.fig
                    if type(oob) == CfgBool:
                        print(cmd_lst)
                        funct = getattr(class_major,cmd_lst[1])
                        funct(oob.cfg[oob.key])
                    if type(oob) == CfgCmd:
                        cmd_lst = oob.key.split('_')
                        print(cmd_lst)
                        funct = getattr(class_major,oob.value)
                        funct(self.npdata[0,:],self.npdata[1,:])
                    if type(oob) == CfgString:
                        cmd_lst = oob.key.split('_')
                        print(cmd_lst)
                        funct = getattr(class_major,cmd_lst[1])
                        funct(oob.cfg[oob.key])
            plt.savefig("img.png")
            self.pixmap = QPixmap().load("img.png")
            self.setImgGroup(self.Parent.tab_layout)
            os.remove("img.png")

   
    def updatePlotData(self):
        self.Open()
        self.check_data_files()
        self.get_averages()
        temp_ary = []
        self.data = pd.read_csv(self.sumFile,header=0)  
        for ii in range(len(self.cfg.fields_array)):
            temp_ary.append(self.data[self.cfg.fields_array[ii]].values)
        self.onpdata = np.array(temp_ary) 
        
        #for ii in range(len(self.cfg.fields_array)):
        self.npdata = self.onpdata[:2,7:20]
         
        self.hasPlot = True
        self.updatePlot()
            

    def updateCfgData(self):
        for oob in self.objArry:
            oob.updateCFGData()
        self.itemcfg.updateCfg()
        self.updatePlotData()
        self.LatexFileImage.Write() 
        

    def OpenLatxCFG(self):
        print(self.itemcfg)
        self.doItems(self.itemcfg.config)
        self.updatePlotData()
    
    
    def setImgGroup(self,layout):
        ## Image Interface
        self.imageGroupLayout = QGridLayout()
        self.Parent.imgmgrp.setLayout(self.imageGroupLayout)
        self.image = QLabel()
        self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,15,15)
        self.imageGroupLayout.addWidget(self.image,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.pixmap = QPixmap("img.png")
        self.setSize(self.Parent.imgmgrp,self.pixmap.height()+50,self.pixmap.width()) 
        self.setSize(self.image,self.pixmap.height()+50,self.pixmap.width()) 
        self.image.setPixmap(self.pixmap)
        return self.Parent.imgmgrp
          
    
    def Open(self):
        match(self.cfg.dataType_text):
            case "PQB":
                self.topdir = self.cfg.data_dir + "/perfdataPQB"
                self.sumFile = self.topdir + "/perfdataPQB.csv"
            case "PCD":
                self.topdir = self.cfg.data_dir + "/perfdataPCD"
                self.sumFile = self.topdir + "/perfdataPCD.csv"
            case "DUP":
                self.topdir = self.cfg.data_dir + "/perfdataDUP"
                self.sumFile = self.topdir + "/perfdataDUP.csv"
            case "CFB":
                self.topdir = self.cfg.data_dir + "/perfdataCFB"
                self.sumFile = self.topdir + "/perfdataCFB.csv"
    
    # Returns true if number of .tst files equal to number of R or D files
    def check_data_files(self) -> bool:
        if(os.path.exists(self.sumFile) == False):
            print ("Data Direcoptries not available" )
            self.hasRawData = False
            return False
        tst_files = [i for i in os.listdir(self.topdir) if i.endswith(".tst")]
        self.data_files = [i[:-5] for i in os.listdir(self.topdir) if i.endswith("R.csv")]
        self.hasRawData = len(tst_files) == len(self.data_files)
        if(self.hasRawData == False):
            print("Raw data file count error")
        return self.hasRawData
    
    def create_summary(self):
        data = ['Name', 'fps', 'cpums', 'cms', 'gms', 'expectedp', 'loadedp',
                'shaderp_comp', 'shaderp_grph', 'expectedc', 'shaderc', 'sidelen']
        with open(self.sumFile, mode= 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    

    def get_averages(self):
        if(self.hasRawData == False):
            return
        self.create_summary()
        for i in self.data_files:
            file_path_debug = self.topdir + "/" + i + "D.csv"
            file_path_release = self.topdir + "/" + i + "R.csv"
            fps = cpums = cms = gms = expectedp = loadedp = shaderp_comp = shaderp_grph = expectedc = shaderc = sidelen = count = 0
            with open(file_path_debug, 'r') as filename:
                file = csv.DictReader(filename)
                for col in file:
                    count += 1
                    expectedp += float(col['expectedp'])
                    loadedp += float(col['loadedp'])
                    shaderp_comp += float(col['shaderp_comp'])
                    shaderp_grph += float(col['shaderp_grph'])
                    expectedc += float(col[' expectedc'])
                    shaderc += float(col['shaderc'])
                    sidelen += float(col[' sidelen'])
            with open(file_path_release, 'r') as filename:
                file = csv.DictReader(filename)
                for col in file:
                    fps += float(col['fps'])
                    cpums += float(col['cpums'])
                    cms += float(col['cms'])
                    gms += float(col['gms'])
            fps = fps / count
            cpums = cpums / count
            cms = cms / count
            gms = gms / count
            expectedp = expectedp / count
            loadedp = loadedp / count
            shaderp_comp = shaderp_comp / count
            shaderp_grph = shaderp_grph / count
            expectedc = expectedc / count
            shaderc = shaderc / count
            sidelen = sidelen / count
            avg_list = [i, fps, cpums, cms, gms, expectedp, loadedp, shaderp_comp,
                        shaderp_grph, expectedc, shaderc, sidelen]
            with open(self.sumFile, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(avg_list)
            self.average_list.append(avg_list)
        file.close()