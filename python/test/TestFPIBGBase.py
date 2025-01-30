
import sys
syspth = sys.path
# This is the base class
##print(syspth)
#print("=====================================")
sys.path.append("x:\\FPIBGUtility\\python\\shared")
syspth1 = sys.path
#print("=====================================")
#print(syspth1)
import os
cwd = os.getcwd()
print(cwd)

from FPIBGBase import FPIBGBase
print("Start")

baseClass = FPIBGBase("FPIBGFrontEnd")
baseClass.Create("FPIBGFrontEnd")
baseClass.testObject(1)