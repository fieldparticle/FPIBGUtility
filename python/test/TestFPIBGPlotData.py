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
guser = getpass.getuser()                                               #
# Now do imports                                              #
###############################################################

from FPIBGBase import *
from FPIBGPlotData import *

bc = FPIBGBase("GlobalBaseClass")
#bc.Create("ParticleKM.cfg",'KMLog.log')
match guser:
    case "jbwk":
        bc.Create("ParticleJB.cfg",'MyLog.log')
    case _:
        bc.Create("ParticleKM.cfg",'KMLog.log')
myClass = PlotData("ExampleObject")
myClass.Create(bc,"PQB")
myClass.Open()
myClass.plot_cpums()
myClass.plot_B1()
myClass.plot_linearity()
myClass.plot_cell_fraction()
    
bc.Close()
myClass.Close() 