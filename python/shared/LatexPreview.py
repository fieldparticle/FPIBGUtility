import subprocess, os


class LatexPreview():
    fileName = ''
    def __init__(self,fileName,texName,wkdir,valsFile):
        self.fileName = fileName
        self.texName = texName
        self.wkdir = wkdir
        self.valsFile = valsFile
        pass

    def ProcessLatxCode(self):
        dirname = os.path.dirname(self.fileName)
        hdr_file = dirname + "/LatexUtilityBaseHeader.tex"
        hdr_lst = []
        with open(hdr_file,"r") as hfile:
            hdr_lst.append(hfile.readlines())

        fl = open(self.fileName,'w')
        for ii in range(len(hdr_lst)):
            res = ' '.join(hdr_lst[ii])
            fl.write(res)    
        fl.write('\\usepackage{graphicx}\n')
        fl.write('\\usepackage{subcaption}\n')
        fl.write('\\usepackage{makecell}\n')
        fl.write('\\begin{document}\n')
        fl.write("\\input{"  +  self.valsFile  + "}\n")
        texname = "\\input {" + self.texName + "}\n" 
        fl.write(texname)
        fl.write('\\end{document}\n')
        fl.flush()
        fl.close()
    
    def Run(self):
        with open("termPreview.log","w") as outFile:
            x = subprocess.call(f"pdflatex -halt-on-error {self.fileName}",cwd= self.wkdir,stdout=outFile)
            if x != 0:
                print('Exit-code not 0, check result!')
                