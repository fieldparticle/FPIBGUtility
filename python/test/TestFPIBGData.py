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
from FPIBGData import *
bc = FPIBGBase("GlobalBaseClass")
bc.Create("ParticleKM.cfg",'KMLog.log')
myClass = DataClass(True, "ExampleObject")
myClass.Create(bc,"PQB")
myClass.Open()
if (myClass.check_data_files() != True):
    print("Did not work") 
myClass.create_summary()
myClass.get_averages()
print(myClass.average_list)
    
bc.Close()
myClass.Close() 