
import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt
sys.path.append("X:\FPIBGMain\FPIBGUtility\python\shared")
from FPIBGMainWin import *
from FPIBGBase import FPIBGBase
bc = FPIBGBase("FPIBGFrontEnd")
bc.Create("ParticleJB.cfg","FPIBG.log")
#print(sys.path)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FPIBGMainWin("FPIBGMainWin")
    window.Create(bc)
    sys.exit(app.exec())
    
