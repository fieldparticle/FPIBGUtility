from PyQt6.QtCore import Qt,QByteArray
from PyQt6.QtWidgets import QWidget,QScrollArea,QVBoxLayout,QTabWidget
from PyQt6.QtGui import QPixmap,QImage
from CfgLabel import *
from LatexClass import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
import numpy as np
from LatexConfigurationClass import *

class LatexSinglePlot(LatexConfigurationClass):
    fignum = 0
    
    data = None
    hasPlot = False
    npdata = None
    fig = None
    ax = None
    pixmap = None

    def __init__(self,Parent):
        super().__init__(Parent)
        self.Parent = Parent
        self.bobj = self.Parent.bobj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.itemcfg = Parent.itemcfg 
        self.LatexFileImage = LatexPlotWriter(self.Parent)


    def __exit__(self):
        plt.close("all")
  

    def updatePlotData(self):
        self.colcount = 0
        self.linecount = 0
        
        try:
            self.rows = []
            with open(self.itemcfg.config.data_file, mode ='r')as file:
                self.csvFile = csv.reader(file)
                for lines in self.csvFile:
                    if len(lines) != 0:
                        rws = [float(ele) for ele in lines]
                        self.rows.append(rws)
        except BaseException as e:
            print("Error with csv file:",e)
            return
        self.hasPlot = True
        self.npdata = np.array(self.rows)
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
          
    
    
    
 

   