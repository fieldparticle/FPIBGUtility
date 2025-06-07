import subprocess, os

class LatexPreview():
    fileName = ''
    def __init__(self,fileName,texName,wkdir):
        self.fileName = fileName
        self.texName = texName
        self.wkdir = wkdir
        pass

    def ProcessLatxCode(self):
        fl = open(self.fileName,'w')
        fl.write('\\documentclass{article}\n')
        fl.write('\\usepackage{graphicx}')
        fl.write('\\usepackage{subcaption}')
        fl.write('\\begin{document}\n')
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

        