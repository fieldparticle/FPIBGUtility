import io
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from PyQt6.QtGui import QPixmap, QImage
from FPIBGDataEXP import *

class PlotData(DataClass):

    
    
    def __init__(self, ObjName):
        super().__init__(ObjName)
        self.ObjName = ObjName


    def Create(self, BaseObj):
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.testFile = ""
        self.bobj.lvl = 1000

    def Open(self,typeFlag):    
        self.typeFlag = typeFlag
        pass

    def hasData(self):
        return self.hasDataFlag
    
    def Update(self,test) -> bool:

        match(test):
            case "PQB":
                self.topdir = self.cfg.application.testdirPQB
                self.testFile = "perfPQB.csv"
                self.upper = os.path.split(self.topdir)
                self.topdir = self.upper[0] + "/" + self.testFile
                # See if the directory exists
                if (os.path.exists(self.topdir) == True):
                    self.hasDataFlag = True
                else:
                    self.hasDataFlag = False
                    return False
                # Update summary
                if self.UpdateSummary("PQB") == False:
                    return False
                # Read Summary File
                df = pd.read_csv(self.topdir)
                if(len(df) <= 1):
                    self.hasDataFlag = False
                    return False        
                return True
            case "CFB":
                self.topdir = self.cfg.application.testdirPCD
                self.testFile = "perfPCD.csv"
                self.upper = os.path.split(self.topdir)
                self.topdir = self.upper[0] + "/" + self.testFile
                if (os.path.exists(self.topdir) == True):
                    self.hasDataFlag = True
                else:
                    self.hasDataFlag = False
                    return False
                df = pd.read_csv(self.topdir)
                if(len(df) <= 1):
                    self.hasDataFlag = False
                    return False
                if(len(df) <= 1):
                    self.hasDataFlag = False
                    return False
                self.hasDataFlag = True
                return True
            case "DUP":
                self.topdir = self.cfg.application.testdirDUP
                self.testFile = "perfDUP.csv"
                self.upper = os.path.split(self.topdir)
                self.topdir = self.upper[0] + "/" + self.testFile
                if (os.path.exists(self.topdir) == True):
                    self.hasDataFlag = True
                else:
                    self.hasDataFlag = False
                    return False
                df = pd.read_csv(self.topdir)
                if(len(df) <= 1):
                    self.hasDataFlag = False
                    return False
                df = pd.read_csv(self.topdir)
                if(len(df) <= 1):
                    self.hasDataFlag = False
                    return False
                self.hasDataFlag = True
                return True
            case "PCD":
                self.topdir = self.cfg.application.testdirCFB
                self.testFile = "perfCFB.csv"
                self.upper = os.path.split(self.topdir)
                self.topdir = self.upper[0] + "/" + self.testFile
                if (os.path.exists(self.topdir) == True):
                    self.hasDataFlag = True
                else:
                    self.hasDataFlag = False
                    return False
                df = pd.read_csv(self.topdir)
                if(len(df) <= 1):
                    self.hasDataFlag = False
                    return False
                if(len(df) <= 1):
                    self.hasDataFlag = False
                    return False
                self.hasDataFlag = True
                return True

        #self.upper = os.path.split(self.topdir)
        ##self.topdir = self.upper[0] + "/" + self.testFile
        #if (os.path.exists(self.topdir) == True):
         #   self.hasDataFlag = True
        #else:
            #self.hasDataFlag = False
        print(self.topdir)
        pass

    def Close(self):
        pass

    def Read(self):
        pass

    def Write(self):
        pass

    def PlotData(self, name):
        if(self.hasData == False):
            return
        match name:
            # PQB
            case "PQBfpsvn":
                return self.plot_PQBfpsvn()
            # PQB
            case "PQBspfvn":
                return self.plot_PQBspfvn()
            # PQB
            case "PQBlintot":
                return self.plot_PQBlintot()
            # PCD 
            case "spfvside":
                return self.plot_spfvside()
            #CFB
            case "spfvcollisions":
                return self.plot_spfvcollsions()


    def new_path(self, dir):
        parts = dir.rsplit("/", 1) 
        parts[-1] = parts[-1].replace("data", "")
        return "/".join(parts)
    
    def exponential(self, x, a, b):
        return a * np.exp(b*x)

    # Plot cpums vs loadedp
    def plot_cpums(self):
        df = pd.read_csv(self.topdir)

        loadedp = df["loadedp"].values.reshape(-1, 1)
        cpums = df['cpums']

        model = LinearRegression()
        model.fit(loadedp, cpums)
        y_pred = model.predict(loadedp)

        plt.figure(figsize=(8,5))
        plt.scatter(loadedp, cpums, marker='o', color = "cornflowerblue")
        plt.plot(loadedp, y_pred, linestyle = "-", label="cpums vs loadedp", color = "cornflowerblue")
        plt.xlabel("loadedp")
        plt.ylabel("cpums")
        #plt.title(f"{os.path.basename(self.topdir)}: cpums vs loadedp")
        plt.legend()
        plt.grid(True)
        #plt.show()

    # Plot B1
    def plot_PQBspfvn(self,start):
        df = pd.read_csv(self.topdir)
        dflen = len(df)
        df = df[start:dflen]
        loadedp = df["loadedp"].values.reshape(-1, 1)
        gms = df["gms"]
        cms = df["cms"]
        gms_cms = df["gms"] + df["cms"]

        model = LinearRegression()
        model.fit(loadedp, gms)
        y_pred = model.predict(loadedp)
        var_gms = np.var(gms)
        sd_gms = np.std(gms)
        plt.figure(figsize=(8,5))
        plt.scatter(loadedp, gms, marker='o', color="cornflowerblue")
        plt.plot(loadedp, y_pred, linestyle="-", label="gms vs loadedp", color="cornflowerblue")

        model.fit(loadedp, cms)
        y_pred = model.predict(loadedp)
        var_cms = np.var(cms)
        sd_cms = np.std(cms)
        plt.scatter(loadedp, cms, marker='o', color="mediumseagreen")
        plt.plot(loadedp, y_pred, linestyle="-", label="cms vs loadedp", color="mediumseagreen")

        model.fit(loadedp, gms_cms)
        y_pred = model.predict(loadedp)
        var_gms_cms = np.var(gms_cms)
        sd_gms_cms = np.std(gms_cms)
        plt.scatter(loadedp, gms_cms, marker='o', color="orchid")
        plt.plot(loadedp, y_pred, linestyle="-", label="gms+cms vs loadedp", color="orchid")

        plt.xlabel("Number of Particles (q)")
        plt.ylabel("Seconds per frame, spf (ms)")
        #plt.title(f"{os.path.basename(self.topdir)}: B1 Plot")
        plt.legend()
        plt.grid(True)
        buf = io.BytesIO()
        self.spfvnfig = plt.gcf()
        self.spfvnfig.savefig(buf, format='png')
        buf.seek(0)

        image = QImage()
        image.loadFromData(buf.getvalue())
        pixmap = QPixmap.fromImage(image)
        return pixmap
        
        plt.figure(figsize=(8,5))
        plt.bar(["gms", "cms", "gms + cms"], [var_gms, var_cms, var_gms_cms], color=["cornflowerblue", "mediumseagreen", "orchid"])
        plt.ylabel("Variance")
        plt.title("Variance of gms, cms, and gms + cms")
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(8,5))
        plt.bar(["gms", "cms", "gms + cms"], [sd_gms, sd_cms, sd_gms_cms], color=["cornflowerblue", "mediumseagreen", "orchid"])
        plt.ylabel("Standard Deviation")
        plt.title("Standard Deviation of gms, cms, and gms + cms")
        plt.grid(True)
        plt.show()
        
    def plot_PQBfpsvn(self,start):
        df = pd.read_csv(self.topdir)
        if(len(df.index) <= 1):
            return QPixmap
        dflen = len(df)
        df = df[start:dflen]    
        loadedp = df["loadedp"]
        fps = df["fps"]

        plt.figure(figsize=(8,5))
        
        plt.scatter(loadedp, fps, marker='o', color="cornflowerblue")
        params, covariance = curve_fit(self.exponential, loadedp, fps, p0=[2500, -1e-6])
        plt.plot(loadedp, self.exponential(loadedp, *params), linestyle='-', label="fps vs loadedp", color="cornflowerblue")
        plt.xlabel("Number of Particles (q)")
        plt.ylabel("Frames Per Second, fps")
        #plt.title(f"{os.path.basename(self.topdir)}: Frames Per Second vs Loaded Particles")
        plt.legend()
        plt.grid(True)
        self.fpsvnfig = plt
        buf = io.BytesIO()
        self.fpsvnfig = plt.gcf()
        self.fpsvnfig.savefig(buf, format='png')
        buf.seek(0)

        image = QImage()
        image.loadFromData(buf.getvalue())
        pixmap = QPixmap.fromImage(image)
        return pixmap

    # Plot Linearity
    def plot_PQBlintot(self,start):
        df = pd.read_csv(self.topdir)
        dflen = len(df)
        df = df[start:dflen]
        loadedp = df["loadedp"]
        indexes = loadedp >= 82944
        loadedp = loadedp[indexes].values.reshape(-1, 1)
        cms_loadedp = (df['cms'] / df['loadedp'])[indexes]
        gms_loadedp = (df['gms'] / df['loadedp'])[indexes]
        cms_gms_loadedp = ((df['cms'] + df['gms']) / df['loadedp'])[indexes]

        model = LinearRegression()

        model.fit(loadedp, cms_loadedp)
        y_pred = model.predict(loadedp)
        var_cms_loadedp = np.var(cms_loadedp)
        sd_cms_loadedp = np.std(cms_loadedp)
        plt.figure(figsize=(8,5))
        plt.scatter(loadedp, cms_loadedp, marker='o', color="cornflowerblue")
        plt.plot(loadedp, y_pred, linestyle="-", label="(cms/loadedp) vs loadedp", color="cornflowerblue")

        model.fit(loadedp, gms_loadedp)
        y_pred = model.predict(loadedp)
        var_gms_loadedp = np.var(gms_loadedp)
        sd_gms_loadedp = np.std(gms_loadedp)
        plt.scatter(loadedp, gms_loadedp, marker='o', color="mediumseagreen")
        plt.plot(loadedp, y_pred, linestyle="-", label="(gms/loadedp) vs loadedp", color="mediumseagreen")

        model.fit(loadedp, cms_gms_loadedp)
        y_pred = model.predict(loadedp)
        var_cms_gms = np.var(cms_gms_loadedp)
        sd_cms_gms = np.std(cms_gms_loadedp)
        plt.scatter(loadedp, cms_gms_loadedp, marker='o', color="orchid")
        plt.plot(loadedp, y_pred, linestyle="-", label="(cms+gms)/loadedp vs loadedp", color="orchid")
    
        plt.xlabel("Number of Particles")
        plt.ylabel("Linearity")
        #plt.title(f"{os.path.basename(self.topdir)}: Linearity")
        plt.legend()
        plt.grid(True)

        buf = io.BytesIO()
        fig = plt.gcf()
        fig.savefig(buf, format='png')
        buf.seek(0)

        image = QImage()
        image.loadFromData(buf.getvalue())
        pixmap = QPixmap.fromImage(image)
        return pixmap

        plt.figure(figsize=(8,5))
        plt.bar(["cms/loadedp", "gms/loadedp", "(gms + cms)/loadedp"], [var_cms_loadedp, var_gms_loadedp, var_cms_gms],
                color=["cornflowerblue", "mediumseagreen", "orchid"])
        plt.ylabel("Variance")
        plt.title("Variance of cms/loadedp, gms/loadedp, and gms + cms")
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(8,5))
        plt.bar(["cms/loadedp", "gms/loadedp", "(gms + cms)/loadedp"], [sd_cms_loadedp, sd_gms_loadedp, sd_cms_gms],
                color=["cornflowerblue", "mediumseagreen", "orchid"])
        plt.ylabel("Standard Deviation")
        plt.title("Standard Deviation of cms/loadedp, gms/loadedp, and gms + cms")
        plt.grid(True)
        plt.show()

    # Particle Cell Density
    def plot_PCDspfvside(self):
        df = pd.read_csv(self.topdir)

        sidelen = df["sidelen"]
        # print(sidelen)
        cms = df["cms"]
        gms = df["gms"]
        cms_gms = df["cms"] + df["gms"]

        plt.figure(figsize=(8,5))
        
        plt.scatter(sidelen, cms, marker='o', color="cornflowerblue")
        params, covariance = curve_fit(self.exponential, sidelen, cms, p0=[3, 0])
        plt.plot(sidelen, self.exponential(sidelen, *params), linestyle='-', label="cms vs sidelen", color="cornflowerblue")

        plt.scatter(sidelen, gms, marker='o', color="mediumseagreen")
        params, covariance = curve_fit(self.exponential, sidelen, gms, p0=[3, 0])
        plt.plot(sidelen, self.exponential(sidelen, *params), linestyle='-', label="gms vs sidelen", color="mediumseagreen")

        plt.scatter(sidelen, cms_gms, marker='o', color="orchid")
        params, covariance = curve_fit(self.exponential, sidelen, cms_gms, p0=[3, 0])
        plt.plot(sidelen, self.exponential(sidelen, *params), linestyle='-', label="cms+gms vs sidelen", color="orchid")

        plt.xlabel("Side Length")
        plt.ylabel("Seconds per frame, spf (ms)")
        #plt.title(f"{os.path.basename(self.topdir)}: Cell Fraction Benchmark")
        plt.legend()
        plt.grid(True)
        
        buf = io.BytesIO()
        fig = plt.gcf()
        fig.savefig(buf, format='png')
        buf.seek(0)

        image = QImage()
        image.loadFromData(buf.getvalue())
        pixmap = QPixmap.fromImage(image)
        return pixmap

    
    def plot_expectedc(self):
        df = pd.read_csv(self.topdir)
        
        expectedc = df["expectedc"].values.reshape(-1, 1)
        cms = df["cms"]
        gms = df["gms"]

        model = LinearRegression()

        model.fit(expectedc, cms)
        y_pred = model.predict(expectedc)
        var_cms = np.var(cms)
        sd_cms = np.std(cms)
        plt.figure(figsize=(8,5))
        plt.scatter(expectedc, cms, marker='o', color="cornflowerblue")
        plt.plot(expectedc, y_pred, linestyle="-", label="cms vs expectedc", color="cornflowerblue")

        model = LinearRegression()
        model.fit(expectedc, gms)
        y_pred = model.predict(expectedc)
        var_gms = np.var(gms)
        sd_gms = np.std(gms)
        plt.scatter(expectedc, gms, marker='o', color="mediumseagreen")
        plt.plot(expectedc, y_pred, linestyle="-", label="gms vs expectedc", color="mediumseagreen")
        
        plt.xlabel("Number of Collisions (n)")
        plt.ylabel("Seconds Per Frame, spf(s)")
        #plt.title(f"{os.path.basename(self.topdir)}: Seconds Per Frame vs Number of Collisions")
        plt.legend()
        plt.grid(True)
        #plt.show()

        plt.figure(figsize=(8,5))
        plt.bar(["gms", "cms"], [var_gms, var_cms], color=["cornflowerblue", "mediumseagreen"])
        plt.ylabel("Variance")
        #plt.title("Variance of gms and cms")
        plt.grid(True)
        #plt.show()

        plt.figure(figsize=(8,5))
        plt.bar(["gms", "cms"], [sd_gms, sd_cms], color=["cornflowerblue", "mediumseagreen"])
        plt.ylabel("Standard Deviation")
        plt.title("Standard Deviation of gms and cms")
        plt.grid(True)
        #plt.show()

    #Colisons fraction benchmark
    def plot_spfvcollsions(self):
        df = pd.read_csv(self.topdir)

        shaderc = df["shaderc"].values.reshape(-1, 1)
        cms = df['cms']

        plt.figure(figsize=(8,5))
        plt.scatter(shaderc, cms, marker='o', color = "cornflowerblue")
        plt.plot(shaderc, cms, linestyle = "-", label="cms v shaderc", color = "cornflowerblue")
        plt.xlabel("shaderc")
        plt.ylabel("cms")
        #plt.title(f"{os.path.basename(self.topdir)}: cms v shaderc")
        plt.legend()
        plt.grid(True)
        buf = io.BytesIO()
        self.spfvcollision = plt.gcf()
        self.spfvcollision.savefig(buf, format='png')
        buf.seek(0)

        image = QImage()
        image.loadFromData(buf.getvalue())
        pixmap = QPixmap.fromImage(image)
        return pixmap

