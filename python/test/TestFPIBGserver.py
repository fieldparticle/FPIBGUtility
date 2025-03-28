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
from FPIBGServer import TCPIPServer
bc = FPIBGBase("GlobalBaseClass")
bc.Create("ParticleJB.cfg",'JBLog.log')
tcps = TCPIPServer("TCPIP Client")
tcps.Create(bc)
tcps.Open()
tcps.RecieveImgFile()
