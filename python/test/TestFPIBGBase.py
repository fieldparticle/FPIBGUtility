
import sys
syspth = sys.path
sys.path.append("x:\\FPIBGUtility\\python\\shared")
syspth1 = sys.path
import os
cwd = os.getcwd()
from FPIBGBase import FPIBGBase
bc = FPIBGBase("FPIBGFrontEnd")
bc.Create()
# Logging and configuration files are open from this point on.
bc.testObject(1)
bc.Close()