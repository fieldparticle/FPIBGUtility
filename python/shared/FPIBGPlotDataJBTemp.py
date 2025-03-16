import pandas as pd
import os
import matplotlib.pyplot as plt
from LatexClass import *

class PlotData:
    def Create(self, BaseObj, file_end):
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        
        match(file_end):
            case "PQB":
                self.topdir = self.cfg.application.testdirPQB
            case "PCD":
                self.topdir = self.cfg.application.testdirPCD
            case "DUP":
                self.topdir = self.cfg.application.testdirDUP
            case "CFB":
                self.topdir = self.cfg.application.testdirCFB

    def Open(self):
        pass

    def Close(self):
        pass

    def Read(self):
        pass

    def Write(self):
        pass

    def __init__(self, ObjName):
        self.ObjName = ObjName


    def new_path(self, dir):
        parts = dir.rsplit("/", 1) 
        parts[-1] = parts[-1].replace("data", "")
        return "/".join(parts)

    def plotData(self):
        newdir = self.new_path(self.topdir) + ".csv"
        
        df = pd.read_csv(newdir)

        plt.figure(figsize=(8,5))
        plt.plot(df['loadedp'], df['cpums'], marker='o', linestyle='-', label=newdir)
        plt.xlabel("loadedp")
        plt.ylabel("cpums")
        plt.title(f"{os.path.basename(newdir)}: cpums vs loadedp")
        plt.legend()
        plt.grid(True)
        ltx = LatexPlot("LatexClass")
        ltx.Create(self.bobj)
        ltx.caption = "Caption:Plot of cpums vs loadedp"
        ltx.name = "cpumsvloadedp"
        ltx.width = 0
        ltx.height = 0
        ltx.title = "TITLE:Plot of cpums vs loadedp"
        ltx.scale = 0.50
        ltx.fontSize = 10
        ltx.outDirectory = self.cfg.latex_dir
        ltx.float = False
        ltx.placement = "h"
        ltx.Write(plt)

