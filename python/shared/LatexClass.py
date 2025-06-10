from FPIBGLog import FPIBGLog
from FPIBGConfig import FPIBGConfig
#from TableModel import *
import os
import inspect
import matplotlib.pyplot as plt
from ValHandler import *
#############################################################################################
# 						base class LatexClass
#############################################################################################
class LatexClass:

    ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,Parent):
        self.Parent = Parent
        self.bobj = self.Parent.bobj
        self.log = self.bobj.log
        self.cfg = Parent.itemcfg.config 
        self.itemcfg = Parent.itemcfg 
        self.cleanPRE = True
        self.valHandler = ValHandler()

    def setCleanPre(self, flg):
        self.cleanPRE = flg

    def WritePre(self,pre_name):
        cfg = self.Parent.itemcfg.config
        preoutname = cfg.tex_dir + "/" + pre_name +".tex"
        if self.cleanPRE == True:
            p = open(preoutname, "w")
        else:
            p = open(preoutname, "a")
        w = "%%============================================= Plot %s\r"%(cfg.name_text )
        p.write(w)
        w = "Fig. \\ref{fig:%s}\r"%(cfg.name_text)
        p.write(w)
        if len(cfg.tex_dir) == 0:
            loutname = cfg.name_text + ".tex"
        else:
            loutname =  cfg.tex_dir + "/" + cfg.name_text + ".tex"
        w = "\\input{%s}\r"%(loutname)
        p.write(w)
        p.close()    

   
#############################################################################################
# 						class LatexTableWriter
#############################################################################################
class LatexTableWriter(LatexClass):
    
    def __init__(self,Parent):
        super().__init__(Parent)

    def Create(self,data):
        self.data = data
        self.cols = self.data.shape[0]
        self.rows = self.data.shape[1]
        self.table_array  = [[0 for x in range(self.cols)] for y in range(self.rows)] 
        self.setLatexData()
        
    header_arry = []
    
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
            value =  self.data[i][j]
            self.setTableItemArray(str(value),i,j)
            return str(value)
            return 
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

                    
    def SingleTable(self,f):
        f.write("\\begin{table}[%s]\n" % self.cfg.placement_text)
        f.write("\\fontsize{%s}{%s}\\selectfont\n" % (self.cfg.font_size,self.cfg.font_size))
        f.write("\\renewcommand{\\arraystretch}{%s}\n" % (self.cfg.arystretch_text))
        f.write("\\caption{\\textit{")
        f.write(self.cfg.caption_box)
        f.write("}}\n")
        f.write("\\label{tab:%s}\n"%self.cfg.name_text)
        f.write("\\begin{center}\n")
        f.write("\\begin{tabular}\n{")
        for k in range(self.cols):
            f.write("l ")
        f.write("}\n")
        f.write("\\hline \\\\ \n")
        header_key = f"header_array1"
        lsz = len(self.cfg.command_dict[header_key])
        headers = self.cfg.command_dict[header_key]
        if (self.cols != lsz):
            f.close()
            print("No Latex Headers")   
            return 
        for k in range(lsz):
            if(k < lsz-1):
                txt = ""
                txt = "\\makecell{" + headers[k] + "}&"
            else:
                txt = "\\makecell{" + headers[k] + "}"
            f.write(txt)
        
        f.write("\\\\ \\hline\n")

        for i in range(0,self.rows): #,skip):
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



        
    def Write(self):
        loutname = self.cfg.tex_dir + "/" + self.cfg.name_text + ".tex"
        try:
            f = open(loutname, "w")
        except IOError as e:
            print(f"Couldn't write to file ({e})")
            return
        self.SingleTable(f)

        
#############################################################################################
# 						class LatexPlotWriter
#############################################################################################
class LatexPlotWriter(LatexClass):

   ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,Parent):
        ## ObjName contains the name of this object.
        super().__init__(Parent)
 
    def Write(self):
        cfg = self.Parent.itemcfg.config    
        outname = cfg.tex_dir + "/" + cfg.name_text + ".png"
        plt.savefig(outname)
        loutname = cfg.tex_dir + "/" + cfg.name_text + ".tex"
        f = open(loutname, "w")
        w = "\\begin{figure*}[" + cfg.placement_text + "]\r"
        f.write(w)
        w = "\\centering\r"
        f.write(w)
        if len(cfg.tex_dir) == 0:
            loutname = cfg.name_text 
        else:
            loutname = cfg.tex_dir + "/" + cfg.name_text
        w = "\\includegraphics[width=%0.2fin]{%s}\r"%(8.5*float(cfg.scale_text),loutname)
        f.write(w)
        w = "\\captionof{figure}[%s]{\\textit{%s}}\r"%(cfg.title_text,cfg.caption_box)
        f.write(w)
        w = "\\label{fig:%s}\r"%(cfg.name_text)
        f.write(w)
        w = "\\end{figure*}\r"
        f.write(w)
        f.close()
        self.WritePre("pre_plots")
        
     

#############################################################################################
# 						class LatexImageWriter
#############################################################################################
class LatexImageWriter(LatexClass):

  ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,Parent):
        ## ObjName contains the name of this object.
        super().__init__(Parent)
       
    
 
    def Write(self):
        cfg = self.Parent.itemcfg.config
        loutname = cfg.tex_dir + "/" + cfg.name_text + ".tex"
        f = open(loutname, "w")
        w = "\\begin{figure*}[" + cfg.placement_text + "]\r"
        f.write(w)
        w = "\\centering\r"
        f.write(w)
        if len(cfg.tex_dir) == 0:
            loutname = cfg.name_text 
        else:
            loutname = cfg.tex_dir + "/" + cfg.name_text
        w = "\\includegraphics[width=%0.2fin]{%s}\r"%(8.5*float(cfg.scale_text),loutname)
        f.write(w)
        w = "\\captionof{figure}[%s]{\\textit{%s}}\r"%(cfg.title_text,cfg.caption_box)
        f.write(w)
        w = "\\label{fig:%s}\r"%(cfg.name_text)
        f.write(w)
        w = "\\end{figure*}\r"
        f.write(w)
        f.close()
        self.WritePre("pre_plots")
     
      
        pass


#############################################################################################
# 						class LatexMultiImageWriter
#############################################################################################
class LatexMultiImageWriter(LatexClass):


    
   ##  Constructor for the LatexClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,Parent):
        ## ObjName contains the name of this object.
        super().__init__(Parent)
        self.images = []
 
    def Write(self):
        cfg = self.Parent.itemcfg.config
        outfile = cfg.tex_dir + "/" + cfg.name_text + ".tex"
        try:
            f = open(outfile, "w")
        except IOError as e:
            print(f"Couldn't write to file ({e})")
        w ="\\begingroup\n"
        f.write(w)
        w = "\\centering\n"
        f.write(w)
        w = "\\begin{figure*}[" + cfg.placement_text + "]\n"
        f.write(w)
        
        try:
            for ii in range(0,int(self.cfg.num_plots_text)):
                w = "\t\\begin{subfigure}[b]{" + cfg.plot_width_text + "in}\n"
                f.write(w)
                previewTex = f"{cfg.plots_dir}/{cfg.name_text}{ii+1}.png"
                gdir = "".join(previewTex.rsplit(cfg.tex_dir))
                sgdir = ''.join( c for c in gdir if  c not in '/' )
                print(sgdir)    
                w = "\t\t\\includegraphics[width=" +  cfg.plot_width_text +  "in]{" + sgdir + "}\n"
                f.write(w)
                w = "\t\t\\subcaption[" + "" +"]{" + cfg.caption_array[ii] + "}\n"
                f.write(w)
                refname = os.path.splitext(os.path.basename(gdir))[0]
                w = "\t\t\\label{fig:" + refname + "}\n"
                f.write(w)
                w = "\t\\end{subfigure}\n"
                f.write(w)
                w = "\\hspace{" + cfg.hspace_text + "in}\n"
                f.write(w)
            w = "\\captionof{figure}[TITLE:" + cfg.title_text + "]{\\textit{" + cfg.caption_box + "}}\n"
            f.write(w)
            w = "\t\t\\label{fig:" + cfg.name_text + "}\n"
            f.write(w)
            w = "\\end{figure*}\n"
            f.write(w)
            w = "\\endgroup"
            f.write(w)
        except IOError as e:
            print(f"Couldn't write to file ({e})")
            f.close()
            return
        f.close()

     
      
        



