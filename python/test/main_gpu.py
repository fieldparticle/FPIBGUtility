
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
from PySide6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen
from gpu_main_win import *
from FPIBGBase import FPIBGBase

from monitorcontrol import get_monitors
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
    screens = app.screens()
    window = GPUMainWin("FPIBGMainWin")
    screen = screens[2]
    qr = screen.geometry()
    window.move(qr.left(), qr.top())
    window.Create(bc)
    sys.exit(app.exec())
    
