
###############################################################
## Preamble to every script. Will append the shared directory #
import sys                                                    #  
import os                                                     #
syspth = sys.path                                             #
cwd = os.getcwd()                                             #
shrddir = cwd + "\\python\\shared"                            #
sys.path.append(shrddir)                                      #
import getpass
print(getpass.getuser())
guser = getpass.getuser()
# Now do imports                                              #
###############################################################

from FPIBGBase import *
from MyClass import *
# First instanciate a base class and name it
bc = FPIBGBase("GlobalBaseClass")
# Then call create with your configuration file and log file names,
match guser:
    case "jbwk":
        bc.Create("ParticleJB.cfg",'MyLog.log')
  
myClass = MyClass("ExampleObject")
myClass.Create(bc)
myClass.Open()
myClass.testObject(1,5)
bc.Close()
myClass.Close()