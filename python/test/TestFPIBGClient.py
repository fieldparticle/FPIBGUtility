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
from FPIBGclient import TCPIPClient
bc = FPIBGBase("GlobalBaseClass")
bc.Create("ParticleJB.cfg",'JBLog.log')
tcpc = TCPIPClient("TCPIP Client")
tcpc.Create(bc)
tcpc.Open()
tcpc.CommandLoop()
#tcpc.RunLoop()
