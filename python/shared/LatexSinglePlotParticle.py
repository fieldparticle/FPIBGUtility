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
        self.Parent = Parent
        self.LatexFileImage = LatexMultiImageWriter(self.Parent)
    

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
        self.Open()
        self.check_data_files()
        self.get_averages()
        temp_ary = []
        # allocate a attribute dictionary
        fld = AttrDictFields()
        self.data = pd.read_csv(self.sumFile,header=0)  
        for name, df in self.data.items():
            fld[name] = self.data[name]
        pltNum = 1
        for k,v in self.cfg.command_dict.items():
            #print(k,v)
            if "DataFields" in k:
                print("datafiel")
                for ii in range(len(v)):
                    if any(map(lambda char: char in v[ii], "+-/*")):
                        field = eval(v[ii])
                        temp_ary.append(field)
                    else:
                        # Else strip the fld. from the field and get the array at that column name
                        fldtxt = v[ii].split('.')
                        temp_ary.append(self.data[fldtxt[1]])
                    self.onpdata = np.array(temp_ary)   
                self.hasPlot = True
                self.updatePlot(pltNum)
                temp_ary = []
                pltNum+=1

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

    def doPlot(self,plot_obj,plot_num):
        plotString = f"axes{plot_num}"
        fieldsString = f"DataFields{plot_num}"
        plot_cmds = plot_obj.dict["PlotCommands"]
        plot_list = plot_cmds[plot_num-1].split(".")
        class_major = self.getClassMajor(plot_list[0])
        funct = getattr(class_major,(plot_list[1]))
        lines_cmds = plot_obj.dict[fieldsString]
        for ii in range(len(lines_cmds)-1):
            self.line = funct(self.onpdata[0,:],self.onpdata[ii+1,:])
        pltTempImg = f"{self.itemcfg.config.plots_dir}/{self.itemcfg.config.name_text}{plot_num}.png"
        plt.savefig(pltTempImg)
        plt.close("all")          

   
    
    def setImgGroup(self,layout):
        pass
          
    
    def Open(self):
        if ("PQB" or "PCD" or "CFB") in self.cfg.dataType_text:
            self.topdir = self.cfg.data_dir + "/perfdata" + self.cfg.dataType_text
            self.sumFile = self.topdir + "/perfdata" + self.cfg.dataType_text + ".csv"
        else:
            print("Unrecognized Data Type")
            
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