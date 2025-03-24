###############################################################
## Preamble to every script. Will append the shared directory #
import sys                                                    #  
import os                                                     #
syspth = sys.path                                             #
cwd = os.getcwd()                                             #
shrddir = cwd + "\\python\\shared"                            #
sys.path.append(shrddir)                                      #
# Now do imports                                              #
###############################################################

from FPIBGBase import *
from LatexClass import *
from FPIBGData import (DataClass)
from FPIBGPlotDataJBTemp import PlotData
bc = FPIBGBase("TestLatex")
bc.Create("ParticleJB.cfg",'JBLog.log')
testdata = DataClass(True, "PQB")
testdata.Create(bc,"PQB")
testdata.check_data_files()
testdata.create_summary()
testdata.get_averages()
csv_name = "C:/FPIBGData/FPIBGData/perfPQB.csv"
plt = PlotData("Jack Test Plot for latex")
plt.Create(bc, "PQB")
plt.plotData()
