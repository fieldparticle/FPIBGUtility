import sys
syspth = sys.path
sys.path.append("x:\\SPRINT002MOD003\\FPIBGUtility\\python\\shared")
'''Demonstrates triple double quotes
    docstrings and does nothing really.'''
syspth1 = sys.path
import os
cwd = os.getcwd()
from FPIBGBase import *
from MyClass import *
bc = FPIBGBase("GlobalBaseClass")
bc.Create("ParticleJB.cfg",'MyLog.log')
myClass = MyClass("ExampleObject")
myClass.Create(bc)
myClass.Open()
myClass.testObject(1,5)
bc.Close()
myClass.Close()