from FPIBGLog import FPIBGLog
from FPIBGConfig import FPIBGConfig
import os
import inspect


class LatexClass:

    ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,ObjName):
        ## ObjName contains the name of this object.
        self.ObjName = ObjName

    ## Create() for the LatexClass object.
    # \param BaseObj -- (FPIBGBase) this is the global class that contains the log and config file facilities.
    def Create(self,BaseObj):
        ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        # Assign this objects debug level
        self.dlvl = 10000
   
class LatexTable(LatexClass):
    def __init__(self,ObjName):
        self.ObjName = ObjName
        super().__init__(ObjName)        

    

class LatexPlot(LatexClass):

   ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,ObjName):
        ## ObjName contains the name of this object.
        self.ObjName = ObjName
        super().__init__(ObjName)
        self.caption = ""
        self.name = ""
        self.width = 0
        self.height = 0
        self.title = ""
        self.scale = 0
        self.fontSize = 8
        self.outDirectory = "X:/FPIBGDATAPY/plots"
        self.float = False
        self.placement = "h"

    def saveCaption(self,Text):
        capname = self.outDirectory + "/" + self.name + ".cap"     
        f = open(capname, "w")
        f.write(Text)

    def readCapFile(self):
        capname = self.outDirectory + "/" + self.name + ".cap"     
        if os.path.exists(capname):
            f = open(capname, "r")
            return f.read()    
        else:
            f = open(capname, "w")
            f.write("No caption")
            return "No Caption"

        
    def Create(self,outDirectory,pltName):
        self.outDirectory = outDirectory    
        self.name = pltName
      
 
    def Write(self,Plot):
        self.saveCaption(self.caption)
        outname = self.outDirectory + "/" + self.name + ".png"
        Plot.savefig(outname)
        loutname = self.outDirectory + "/" + self.name + ".tex"
        f = open(loutname, "w")
        w = "\\begin{figure*}[" + self.placement + "]\r"
        f.write(w)
        w = "\\centering\r"
        f.write(w)
        w = "\\includegraphics[width=%0.2fin]{%s}\r"%(8.5*self.scale,outname)
        f.write(w)
        w = "\\captionof{figure}[%s]{\\textit{%s}}\r"%(self.title,self.caption)
        f.write(w)
        w = "\\label{fig:%s}\r"%(self.name)
        f.write(w)
        w = "\\end{figure*}\r"
        f.write(w)
        f.close()
        preoutname = self.outDirectory + "/" + "pre_plots.tex"
        p = open(preoutname, "w")
        w = "%%============================================= Plot %s\r"%(self.name)
        p.write(w)
        w = "Fig. \\ref{fig:%s}\r"%(self.name)
        p.write(w)
        w = "\\input{%s}\r"%(loutname)
        p.write(w)
        p.close()
        pass




