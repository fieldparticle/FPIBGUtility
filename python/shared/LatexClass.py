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

    def setPlacment(self,pl):
        self.placement = pl

    def setFontSize(self,fsz):
        self.fontSize = fsz

    def setArrayStretch(self,st):
        self.arrayStretch = st

    def saveCaption(self,Text):
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
        
    def WritePre(self,mode):
        preoutname = self.outDirectory + "/" + "pre_tables.tex"
        p = open(preoutname, "w")
        w = "%%============================================= Plot %s\r"%(self.name)
        p.write(w)
        w = "Fig. \\ref{fig:%s}\r"%(self.name)
        p.write(w)
        loutname = self.outDirectory + "/" + self.name + ".tex"
        w = "\\input{%s}\r"%(loutname)
        p.write(w)
        p.close()    

    def Create(self,outDirectory,pltName):
        self.outDirectory = outDirectory    
        self.name = pltName
      


class LatexTable(LatexClass):
    def __init__(self,data):
        super().__init__()   
        self.data = data
        
        self.outDirectory = "J:/FPIBGDATAPY/tables"
        

    header_arry = []
    

    def Create(self,rows,cols,fileName):
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
                self.setTableItemArray(str("%.0f" % (1000*value)),i,j)
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

                    

    def WriteLatexTable(self):
        self.readCapFile()
        #self.saveCaption(self.caption)
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

        for i in range(self.rows):
            for j in range(self.cols):
                if(j < self.cols-1):
                    txt = str(self.table_array[i][j]) + "&"
                    f.write(txt)
                else:
                    txt = str(self.table_array[i][j]) + "\\\\ \n"
                    f.write(txt)
        f.write("\\hline\n\\end{tabular}\n\\end{center}\n\\end{table}\n")
        f.close()
        self.WritePre("append")


    

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
        self.outDirectory = "X:/FPIBGDATAPY/plots"
        self.float = False
        self.placement = "h"

   
 
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
      
        pass




