import pandas as pd
import os
import matplotlib.pyplot as plt

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


    def plotData(self):
        data_files = [i for i in os.listdir(self.topdir) if i.endswith("D.csv")]

        for file in data_files:
            file_path = os.path.join(self.topdir, file)
            df = pd.read_csv(file_path)

            plt.figure(figsize=(8,5))
            plt.plot(df['loadedp'], df['cpums'], marker='o', linestyle='-', label=file)
            plt.xlabel("loadedp")
            plt.ylabel("cpums")
            plt.title(f"{file}: cpums vs loadedp")
            plt.legend()
            plt.grid(True)
            plt.show()