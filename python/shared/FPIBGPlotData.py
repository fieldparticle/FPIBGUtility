import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

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
        newdir = self.new_path(self.topdir) + ".csv"
        self.topdir = os.path.join(self.topdir, newdir)

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

    # Plot cpums vs loadedp
    def plot_cpums(self):
        df = pd.read_csv(self.topdir)

        plt.figure(figsize=(8,5))
        plt.plot(df['loadedp'], df['cpums'], marker='o', linestyle='-', label="cpums vs loadedp")
        plt.xlabel("loadedp")
        plt.ylabel("cpums")
        plt.title(f"{os.path.basename(self.topdir)}: cpums vs loadedp")
        plt.legend()
        plt.grid(True)
        plt.show()

    # Plot B1
    def plot_B1(self):
        df = pd.read_csv(self.topdir)

        plt.figure(figsize=(8,5))
        plt.plot(df['loadedp'], df['gms'], marker='o', linestyle='-', label="gms vs loadedp")
        plt.plot(df['loadedp'], df['cms'], marker='o', linestyle="-", label="cms vs loadedp")
        plt.plot(df['loadedp'], df['cms'] + df['gms'], marker='o', linestyle="-", label="(cms+gms) vs loadedp")
        plt.xlabel("Number of Particles (q)")
        plt.ylabel("Seconds per frame, spf (ms)")
        plt.title(f"{os.path.basename(self.topdir)}: B1 Plot")
        plt.legend()
        plt.grid(True)
        plt.show()

    # Plot Linearity
    def plot_linearity(self):
        df = pd.read_csv(self.topdir)

        plt.figure(figsize=(8,5))
        plt.plot(df['loadedp'], df['cms'] / df['loadedp'], marker='o', linestyle="-", label="(cms/loadedp) vs loadedp")
        plt.plot(df['loadedp'], df['gms'] / df['loadedp'], marker='o', linestyle="-", label="(gms/loadedp) vs loadedp")
        plt.plot(df['loadedp'], (df['cms'] + df['gms']) / df['loadedp'], marker='o', 
                 linestyle="-", label="(cms+gms)/loadedp vs loadedp")     
        plt.xlim(82944)
        plt.xlabel("Number of Particles")
        plt.ylabel("Linearity")
        plt.title(f"{os.path.basename(self.topdir)}: Linearity")
        plt.legend()
        plt.grid(True)
        plt.show()

    # Plot Cell Fraction Benchmark
    def plot_cell_fraction(self):
        df = pd.read_csv(self.topdir)

        plt.figure(figsize=(8,5))
        plt.plot(df['sidelen'], df['cms'], marker='o', linestyle='-', label="cms vs sidelen")
        plt.plot(df['sidelen'], df['gms'], marker='o', linestyle="-", label="gms vs sidelen")
        plt.plot(df['sidelen'], df['cms'] + df['gms'], marker='o', linestyle="-", label="(cms+gms) vs sidelen")
        plt.xlabel("Side Length")
        plt.ylabel("Seconds per frame, spf (ms)")
        plt.title(f"{os.path.basename(self.topdir)}: Cell Fraction Benchmark")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_fps_vs_loadedp(self):
        df = pd.read_csv(self.topdir)

        plt.figure(figsize=(8,5))
        plt.plot(df['loadedp'], df['fps'], marker='o', linestyle='-', label="fps vs loadedp")
        plt.xlabel("Number of Particles (q)")
        plt.ylabel("Frames Per Second, fps")
        plt.title(f"{os.path.basename(self.topdir)}: Frames Per Second vs Loaded Particles")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_expectedc(self):
        df = pd.read_csv(self.topdir)
        
        plt.figure(figsize=(8,5))
        plt.plot(df['expectedc'], df['cms'], marker='o', linestyle='-', label="cms vs loadedp")
        plt.plot(df['expectedc'], df['gms'], marker='o', linestyle='-', label="gms vs loadedp")
        plt.xlabel("Number of Collisions (n)")
        plt.ylabel("Seconds Per Frame, spf(s)")
        plt.title(f"{os.path.basename(self.topdir)}: Seconds Per Frame vs Number of Collisions")
        plt.legend()
        plt.grid(True)
        plt.show()