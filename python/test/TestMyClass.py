
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
from MyClass import *
# First create a base class and name it
bc = FPIBGBase("GlobalBaseClass")
bc.Create("ParticleJB.cfg",'MyLog.log')
myClass = MyClass("ExampleObject")
myClass.Create(bc)
myClass.Open()
myClass.testObject(1,5)
bc.Close()
myClass.Close()