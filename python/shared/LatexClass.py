from FPIBGLog import FPIBGLog
from FPIBGConfig import FPIBGConfig
#from TableModel import *
import os
import inspect


class LatexClass:

    ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self):
        self.caption = ""
        self.name = ""
        self.width = 0
        self.height = 0
        self.title = ""
        self.scale = 0
        self.fontSize = 8
        self.float = False
        self.placement = "h"
        self.arrayStretch = 1.60
        self.outDirectory = ""
        self.ltxDirectory = ""
        self.cleanPRE = True
        self.caption = ""

    def setPlacment(self,pl):
        self.placement = pl

    def setFontSize(self,fsz):
        self.fontSize = fsz

    def setArrayStretch(self,st):
        self.arrayStretch = st

    def saveCaption(self,Text):
        if not os.path.exists(self.outDirectory):
            os.makedirs(self.outDirectory)
        capname = self.outDirectory + "/" + self.name + ".cap"     
        f = open(capname, "w")
        f.write(Text)

    def readCapFile(self):
        
        capname = self.outDirectory + "/" + self.name + ".cap"     
        if os.path.exists(capname):
            f = open(capname, "r")
            buf= f.read()    
            f.close()
            return buf
        else:
            # Commented this out to prevent errors trying to open a file that doesn't exist
            # f = open(capname, "w")
            # f.write("No caption")
            # f.close()            
            return "No Caption"
        
    
    def WritePre(self,pre_name):
        if not os.path.exists(self.outDirectory):
            os.makedirs(self.outDirectory)
        preoutname = self.outDirectory + "/" + pre_name +".tex"
        if self.cleanPRE == True:
            p = open(preoutname, "w")
        else:
            p = open(preoutname, "a")
        w = "%%============================================= Plot %s\r"%(self.name)
        p.write(w)
        w = "Fig. \\ref{fig:%s}\r"%(self.name)
        p.write(w)
        if len(self.ltxDirectory) == 0:
            loutname = self.name + ".tex"
        else:
            loutname = self.ltxDirectory + "/" + self.name + ".tex"
        w = "\\input{%s}\r"%(loutname)
        p.write(w)
        p.close()    

   
      


class LatexTable(LatexClass):
    def __init__(self,BaseObj,data):
        super().__init__()   
        self.data = data
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log 
        
        

    header_arry = []
    

    def Create(self,rows,cols,fileName):
        self.name = fileName
       
        # Assign this objects debug level
        self.dlvl = 10000
        self.table_array  = [[0 for x in range(cols)] for y in range(rows)] 
        self.rows = rows
        self.cols = cols
        self.name = fileName
        self.setLatexData()
        
    
    def setLatexHeaderArray(self, header):
        self.header_arry = header

    def setTableItemArray(self, cellstr,col, row):
        self.table_array[row][col] = cellstr
        

    def setLatexData(self):
        
        for i in range(self.cols):
            for j in range(self.rows):
                self.loadItem(i,j)

    def loadItem(self,i,j):
            cellstr = ""
            value =  self.data.values[j][i]
            if (i == 0):
                self.setTableItemArray(str("%.0f" % value),i,j)
                return "%.0f" % value
                
            if (i == 1):
                self.setTableItemArray(str("%.2f" % (1000*value)),i,j)
                return "%.2f" % (1000*value)
            
            if (i == 2):
                self.setTableItemArray(str("%.2f" % (1000*value)),i,j)
                return "%.2f" % (1000*value)
            
            if (i == 3):
                self.setTableItemArray(str("%.2f" % (1000*value)),i,j)
                return "%.2f" % (1000*value)
            
            if (i == 4):
                self.setTableItemArray(str("%d" % value),i,j)
                return "%d" % (value)

                    

    def WriteLatexTable(self,skip):
        self.readCapFile()
        #self.saveCaption(self.caption)
        if not os.path.exists(self.outDirectory):
            os.makedirs(self.outDirectory)
           
        loutname = self.outDirectory + "/" + self.name + ".tex"
        f = open(loutname, "w")
        f.write("\\begin{table}[%s]\n" % self.placement)
        f.write("\\fontsize{%d}{%d}\\selectfont\n" % (self.fontSize,self.fontSize))
        f.write("\\renewcommand{\\arraystretch}{%0.2f}\n" % (self.arrayStretch))
        f.write("\\caption{\\textit{")
        f.write(self.readCapFile())
        f.write("}}\n")
        f.write("\\label{tab:%s}\n"%self.name)
        f.write("\\begin{center}\n")
        f.write("\\begin{tabular}\n{")
        for k in range(self.cols):
            f.write("l ")
        f.write("}\n")
        f.write("\\hline \\\\ \n")
        lsz = len(self.header_arry)
        if (self.cols != lsz):
            f.close()
            print("No Latex Headers")    
        for k in range(lsz):
            if(k < lsz-1):
                txt = ""
                txt = "\\makecell{" + self.header_arry[k] + "}&"
            else:
                txt = "\\makecell{" + self.header_arry[k] + "}"
            f.write(txt)
        
        f.write("\\\\ \\hline\n")

        for i in range(0,self.rows,skip):
            for j in range(self.cols):
                if(j < self.cols-1):
                    txt = str(self.table_array[i][j]) + "&"
                    f.write(txt)
                else:
                    txt = str(self.table_array[i][j]) + "\\\\ \n"
                    f.write(txt)
        f.write("\\hline\n\\end{tabular}\n\\end{center}\n\\end{table}\n")
        f.close()
        self.WritePre("pre_tables")


    

class LatexPlot(LatexClass):

   ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,ObjName):
        ## ObjName contains the name of this object.
        self.ObjName = ObjName
        super().__init__()
        self.caption = ""
        self.name = ""
        self.width = 0
        self.height = 0
        self.title = ""
        self.scale = 0
        self.fontSize = 8
        self.float = False
        self.placement = "h"

    def Create(self,BaseObj,Name):
     
        self.name = Name
         ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        # Assign this objects debug level
        self.dlvl = 10000
      
 
    def Write(self,Plot):
        self.saveCaption(self.caption)
        if not os.path.exists(self.outDirectory):
            os.makedirs(self.outDirectory)
        outname = self.outDirectory + "/" + self.name + ".png"
        Plot.savefig(outname)
        loutname = self.outDirectory + "/" + self.name + ".tex"
        f = open(loutname, "w")
        w = "\\begin{figure*}[" + self.placement + "]\r"
        f.write(w)
        w = "\\centering\r"
        f.write(w)
        if len(self.ltxDirectory) == 0:
            loutname = self.name + ".png"
        else:
            loutname = self.ltxDirectory + "/" + self.name + ".png"
        w = "\\includegraphics[width=%0.2fin]{%s}\r"%(8.5*self.scale,loutname)
        f.write(w)
        w = "\\captionof{figure}[%s]{\\textit{%s}}\r"%(self.title,self.caption)
        f.write(w)
        w = "\\label{fig:%s}\r"%(self.name)
        f.write(w)
        w = "\\end{figure*}\r"
        f.write(w)
        f.close()
        self.WritePre("pre_plots")
     
      

class LatexImage(LatexClass):

   ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,ObjName):
        ## ObjName contains the name of this object.
        self.ObjName = ObjName
        super().__init__()
        self.caption = ""
        self.name = ""
        self.width = 0
        self.height = 0
        self.title = ""
        self.scale = 0
        self.fontSize = 8
        self.float = False
        self.placement = "h"
        self.type = ""

    def Create(self,BaseObj,Name):
     
        self.name = Name
         ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        # Assign this objects debug level
        self.dlvl = 10000
      
 
    def Write(self,cfg):
        self.saveCaption(self.caption)
        if not os.path.exists(self.outDirectory):
            os.makedirs(self.outDirectory)
        outname = self.outDirectory + "/" + cfg.name_text + ".png"
        loutname = self.outDirectory + "/" + cfg.name_text + ".tex"
        f = open(loutname, "w")
        w = "\\begin{figure*}[" + self.placement + "]\r"
        f.write(w)
        w = "\\centering\r"
        f.write(w)
        if len(self.ltxDirectory) == 0:
            loutname = cfg.images_name_text 
        else:
            loutname = self.ltxDirectory + "/" + cfg.images_name_text
        w = "\\includegraphics[width=%0.2fin]{%s}\r"%(8.5*float(self.scale),loutname)
        f.write(w)
        w = "\\captionof{figure}[%s]{\\textit{%s}}\r"%(self.title,self.caption)
        f.write(w)
        w = "\\label{fig:%s}\r"%(cfg.name_text)
        f.write(w)
        w = "\\end{figure*}\r"
        f.write(w)
        f.close()
        self.WritePre("pre_plots")
     
      
        pass



class LatexMultiImage(LatexClass):


    
   ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,ObjName):
        ## ObjName contains the name of this object.
        self.ObjName = ObjName
        super().__init__()
        self.caption = ""
        self.name = ""
        self.width = 0
        self.height = 0
        self.title = ""
        self.scale = 0
        self.fontSize = 8
        self.float = False
        self.placement = "h"
        self.type = ""
        self.images = []
        

    def Create(self,BaseObj,Name):
        self.name = Name
         ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        # Assign this objects debug level
        self.dlvl = 10000

    def Update(self,cfg):
        pass

 
    def Write(self,cfg):
        pass
        self.saveCaption(self.caption)
        if not os.path.exists(self.outDirectory):
            os.makedirs(self.outDirectory)
        f = open(loutname, "w")
        w = "\\begin{figure*}[" + self.placement + "]\r"
        f.write(w)
        w = "\\centering\r"
        f.write(w)
        loutname = self.ltxDirectory + "/" + cfg.images_name_text
        w = "\\includegraphics[width=%0.2fin]{%s}\r"%(8.5*float(self.scale),loutname)
        f.write(w)
        w = "\\captionof{figure}[%s]{\\textit{%s}}\r"%(self.title,self.caption)
        f.write(w)
        w = "\\label{fig:%s}\r"%(cfg.name_text)
        f.write(w)
        w = "\\end{figure*}\r"
        f.write(w)
        f.close()
        #self.WritePre("pre_plots")
     
      
        pass



