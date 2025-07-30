
class ValHandler:
    
    def __init__(self):
        pass

    def appendValues(self,macro,val):
        valstr = "\\newcommand{\\" + macro + "}{" + val + "}\n"
        fl = open(self.fileName,'a')
        fl.write(valstr)
        fl.close()

    def doValues(self,fileName):
        self.fileName = fileName
        fl = open(self.fileName,'w')
        fl.write('\\newcommand{\\bestTime}{25 fps}\n')
        fl.write('\\newcommand{\\bestNumberParts}{4,375,552}\n')
        fl.write('\\newcommand{\\bestNumberQueries}{$9.5727x10^{12}$}\n')
        fl.close()


