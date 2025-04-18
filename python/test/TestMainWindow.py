
###############################################################
## Preamble to every script. Will append the shared directory #
import sys                                                    #  
import os                                                     #
syspth = sys.path                                             #
cwd = os.getcwd()                                             #
shrddir = cwd + "\\python\\shared"                            #
sys.path.append(shrddir)           
import getpass                                                #
print(getpass.getuser())                                      #
guser = getpass.getuser()                            #
# Now do imports                                              #
###############################################################
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt
from FPIBGMainWin import *
from FPIBGBase import FPIBGBase
## Create a base class.
bc = FPIBGBase("FPIBGFrontEnd")
 
match guser:
    case "jbwk":
        bc.Create("ParticleJB.cfg",'FPIBGJB.log')
    case _:
        bc.Create("ParticleKM.cfg",'KMLog.log')

#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FPIBGMainWin("FPIBGMainWin")
    window.Create(bc)
    sys.exit(app.exec())
    
