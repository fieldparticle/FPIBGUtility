from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from CfgLabel import *
from LatexClass import *
import pandas as pd
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

    def __init__(self,Parent,itemCFG=None):
        super().__init__(Parent)
        self.LatexFileImage = LatexMultiImageWriter(self.Parent)


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
        temp_ary = []
        self.data = pd.read_csv(self.cfg.data_file,header=0)  
        for ii in range(len(self.cfg.fields_array)):
            temp_ary.append(self.data[self.cfg.fields_array[ii]].values)
        self.npdata = np.array(temp_ary)  
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
       pass
          
    
    
    
 

   