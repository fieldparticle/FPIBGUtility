
###############################################################
## Preamble to every script. Will append the shared directory #
import sys                                                    #  
import os                                                     #
syspth = sys.path                                             #
cwd = os.getcwd()                   
print(cwd)                          #
shrddir = cwd + "\\python\\shared"                            #
sys.path.append(shrddir)           
shrddir = cwd + "\\python\\test"                            #
sys.path.append(shrddir)           
import getpass                                                #
print(getpass.getuser())                                      #
guser = getpass.getuser()                            #
# Now do imports                                              #
###############################################################
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt
from FPIBGLatexWin import *
from FPIBGBase import *
import matplotlib
## Create a base class.
bc = FPIBGBase("FPIBGFrontEnd")
print("Hello World\n", file=sys.stdout)
bc.Create("ParticleJB.cfg",'FPIBGJB.log')

if __name__ == '__main__':
    f = matplotlib.matplotlib_fname()
    print(f)
    app = QApplication(sys.argv)
    screens = app.screens()
    window = FPIBGLatexWin(bc,"FPIBGMainWin")
    screen = screens[3]
    qr = screen.geometry()
    window.move(qr.left(), qr.top())
    window.Create(bc)
    sys.exit(app.exec())
    
