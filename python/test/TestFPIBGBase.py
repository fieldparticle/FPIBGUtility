
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
from FPIBGBase import FPIBGBase
bc = FPIBGBase("GlobalBaseClass")
bc.Create("ParticleJB.cfg","FPIBGLogJB.log")

# Logging and configuration files are open from this point on.
bc.testObject(1,5)
bc.testObject(2,5)
bc.Close()