
import sys
syspth = sys.path
sys.path.append("x:\\FPIBGMain\\FPIBGUtility\\python\\shared")
'''Demonstrates triple double quotes
    docstrings and does nothing really.'''
syspth1 = sys.path
import os
cwd = os.getcwd()
from FPIBGBase import FPIBGBase
bc = FPIBGBase("GlobalBaseClass")
#help(FPIBGBase)
#print("Using __doc__:")
#print(FPIBGBase.Create.__doc__)
bc.Create()
# Logging and configuration files are open from this point on.
bc.testObject(1,5)
bc.testObject(2,5)
bc.Close()