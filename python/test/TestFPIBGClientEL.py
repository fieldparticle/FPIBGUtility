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
from FPIBGclient import TCPIP
bc = FPIBGBase("GlobalBaseClass")
bc.Create("ParticleEL.cfg",'ELLog.log')
tcpc = TCPIP("TCPIP Client")
tcpc.Create(bc)
tcpc.Open()
tcpc.CommandLoop()
#tcpc.RunLoop()
