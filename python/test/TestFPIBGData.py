###############################################################
## Preamble to every script. Will append the shared directory #
import sys                                                    #  
import os                                                     #
syspth = sys.path                                             #
cwd = os.getcwd()                                             #
shrddir = cwd + "\\python\\shared"                            #
sys.path.append(shrddir)                                      #
import getpass                                                #
print(getpass.getuser())                                      #
guser = getpass.getuser()                                     #
# Now do imports                                              #
###############################################################

from FPIBGBase import *
from FPIBGData import *
bc = FPIBGBase("GlobalBaseClass")
match guser:
    case "jbwk":
        bc.Create("ParticleJB.cfg",'MyLog.log')
    case _:
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