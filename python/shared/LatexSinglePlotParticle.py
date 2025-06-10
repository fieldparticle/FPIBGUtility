from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QGroupBox,QMessageBox,QDialog
from CfgLabel import *
from LatexClass import *
import pandas as pd
import cycler
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
import numpy as np
from LatexConfigurationClass import *
from LatexSinglePlot import * 
from FPIBGConfig import *
from AttrDictFields import *
from LatexPreview import *
from LatexDialogs import *
from TrendLine import *
from ValHandler import *
from LatexDataContainer import *
class LatexSinglePlotParicle(LatexSinglePlot):
    fignum = 0
    
    
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
        self.Parent = Parent
        self.LatexFileImage = LatexMultiImageWriter(self.Parent)
        self.valHandler = ValHandler()
    

    def isfloat(self,value):
        try:
            return isinstance(float(value), float) and '.' in value
        except ValueError:
            return False
   
    def isInt(self,val):
        if val.isdigit():
            return True
        else:
            return False
    
    def preview(self):
      pass
        
    def getClassMajor(self,ClasStr):
        match(ClasStr):
            case "ax":
                return self.ax
            case "plt":
                return plt
            case "fig":
                return self.fig

    def __exit__(self):
        plt.close("all")
      
   
    # Decode plot rcParams to configure the plot
    def doDictionary(self,oob,class_major,PlotNum):
        formatString = f"plotFormat{PlotNum}"
        axisString = f"axes{PlotNum}"
        for k,v in oob.dict.items():
            if formatString in k:
                for ii in range(len(v)):
                    all_item = v[ii].split("=")
                    cmd_item = all_item[0]
                    val_item = all_item[1]
                    if "prop.prop_cycle" in v[ii]:
                        try : 
                            colors = list(v[ii].split(","))
                            color_cycle = cycler.cycler(color=colors)
                            self.ax.set_prop_cycle(color_cycle)
                            continue
                        except BaseException as e:
                            print(e)
                            continue
                    try :
                        if self.isfloat(val_item) == True:
                            plt.rcParams[cmd_item]= float(val_item)
                        elif self.isInt(val_item) == True:
                            plt.rcParams[cmd_item] = int(val_item)
                        else:
                            plt.rcParams[cmd_item] = str(val_item)
                    except BaseException as e:
                        print(e)
                        continue
            if axisString in k:
                for ii in range(len(v)):
                    all_item = v[ii].split("=")
                    cmd_list = all_item[0]
                    cmd_item = cmd_list.split(".")
                    val_item = all_item[1]
                    funct = getattr(self.getClassMajor(cmd_item[0]),cmd_item[1].strip())
                    funct(val_item)
            
    def updateCfgData(self):
        for oob in self.objArry:
            oob.updateCFGData()
        self.itemcfg.updateCfg()
        self.updatePlotData()
        self.LatexFileImage.Write() 
        

    def OpenLatxCFG(self):
        #print(self.itemcfg)
        self.doItems(self.itemcfg.config)
        self.updatePlotData()

    def updatePlotData(self):
        self.valHandler.doValues(f"{self.itemcfg.config.tex_dir}/vals.tex")            
        # for each plot line
        for plotNum in range(1,int(self.cfg.num_plots_text)+1):
            temp_ary = []
            # allocate a attribute dictionary
            fld = AttrDictFields()
            dataObj = LatexDataContainer(self.bobj,"LatexDataContainer")
            data_src = self.cfg.command_dict.DataSource[plotNum-1]
            dataObj.Create(data_src,self.cfg.data_dir)
            data = dataObj.getData()
            print(data_src)
            print(data)
            for name, df in data.items():
                fld[name] = data[name]
            plotGrouptxt = "DataFields" + str(plotNum)
            data_fields = self.cfg.command_dict[plotGrouptxt]
            for ii in range(len(data_fields)):
                if any(map(lambda char: char in data_fields[ii], "+-/*")):
                    field = eval(data_fields[ii])
                    temp_ary.append(field)
                else:
                    # Else strip the fld. from the field and get the array at that column name
                    fldtxt = data_fields[ii].split('.')
                    temp_ary.append(data[fldtxt[1]])
                self.onpdata = np.array(temp_ary)   
            self.hasPlot = True
            self.updatePlot(plotNum)
            temp_ary = []
                  

    def updatePlot(self,PlotNum):
        if(self.fignum != 0):
            plt.close("all")
        self.fignum += 1
        self.fig = plt.figure(self.fignum)
        self.ax = self.fig.gca()
        if self.hasPlot == True:
            plot_obj = None
            for oob in self.objArry:
                cmd_lst = oob.key.split('_')
                matches = ["plt","ax","fig","command"]
                class_major = None
                class_major = self.getClassMajor(cmd_lst[0])
                if any(x in cmd_lst[0] for x in matches):
                    if type(oob) == CfgDict:
                        plot_obj = oob
                        self.doDictionary(oob,class_major,PlotNum)
                    if type(oob) == CfgBool:
                        #print(cmd_lst)
                        funct = getattr(class_major,cmd_lst[1])
                        funct(oob.cfg[oob.key])
                    if type(oob) == CfgString:
                        cmd_lst = oob.key.split('_')
                        #print(cmd_lst)
                        funct = getattr(class_major,cmd_lst[1])
                        funct(oob.cfg[oob.key])
            self.doPlot(plot_obj,PlotNum)

    # Plot and save temp image
    def doPlot(self,plot_obj,plot_num):
        sslice = self.itemcfg.config.data_start_text
        if self.isInt(sslice) == True:
            sslice = int(sslice)
        eslice = self.itemcfg.config.data_end_text
        if self.isInt(eslice) == True:
            eslice = int(eslice)
        plotString = f"axes{plot_num}"
        fieldsString = f"DataFields{plot_num}"

        # Convert text plot command to function
        cmd_txt = f"PlotCommands{plot_num}"
        plot_cmds = plot_obj.dict[cmd_txt]
        plot_list = plot_cmds[plot_num-1].split(".")
        class_major = self.getClassMajor(plot_list[0])
        funct = getattr(class_major,(plot_list[1]))
        lines_cmds = plot_obj.dict[fieldsString]

        # Get color. Its special becasue it has no rcParams
        line_key = f"LineColors{plot_num}"
        line_colors = plot_obj.dict[line_key]

        # Do the plot
        for ii in range(len(lines_cmds)-1):
            self.line = funct(self.onpdata[0,sslice:],self.onpdata[ii+1,sslice:],color=line_colors[ii])
        
        # Do trendline
        trendString = f"Trendline{plot_num}"
        trendcmd = plot_obj.dict[trendString][plot_num-1]
        nameKey = f"PlotNames{plot_num}"
        pltname = plot_obj.dict[nameKey]
        if not "none" in trendcmd:
            for zz in range(len(lines_cmds)-1):
                trend  = TrendLine(self.onpdata[0,sslice:],self.onpdata[zz+1,sslice:],trendcmd,pltname[zz],self.valHandler)
                trend.doTrendLine(plt,line_colors[zz])
                


        # Do the Legend
        legendtxt = "Legend" + str(plot_num)
        leggroup = self.cfg.command_dict[legendtxt]
        self.ax.legend(leggroup)

        # Save temp image 
        pltTempImg = f"{self.itemcfg.config.plots_dir}/{self.itemcfg.config.name_text}{plot_num}.png"
        plt.savefig(pltTempImg, bbox_inches='tight')
        plt.close("all")          

   
    
    def setImgGroup(self,layout):
        pass
          
   