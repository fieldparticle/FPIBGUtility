
import sys
syspth = sys.path
sys.path.append("x:\\SPRINT002MOD003\\FPIBGUtility\\python\\shared")
'''Demonstrates triple double quotes
    docstrings and does nothing really.'''
syspth1 = sys.path
import os
cwd = os.getcwd()
from FPIBGBase import FPIBGBase
bc = FPIBGBase("GlobalBaseClass")
bc.Create("Particle.cfg","MyLog.log")

# Logging and configuration files are open from this point on.
bc.testObject(1,5)
bc.testObject(2,5)
bc.Close()