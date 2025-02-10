
import sys
import os
syspth = sys.path
sys.path.append("x:\\FPIBGUtility\\python\\shared")
'''Demonstrates triple double quotes
    docstrings and does nothing really.'''
from pptimg2md  import pptimg2md
syspth1 = sys.path

cwd = os.getcwd()

bc = pptimg2md("X:\\doc\\FPIBGProjectSec001","X:\\doc\\Sect001.md")
bc.Open()
bc.Close()

bc = pptimg2md("X:\\doc\\FPIBGProjectSec002","X:\\doc\\Sect002.md")
bc.Open()
bc.Close()

bc = pptimg2md("X:\\doc\\FPIBGProjectSec003","X:\\doc\\Sect003.md")
bc.Open()
bc.Close()

bc = pptimg2md("X:\\doc\\FPIBGProjectSec004","X:\\doc\\Sect004.md")
bc.Open()
bc.Close()

bc = pptimg2md("X:\\doc\\FPIBGSprint001","X:\\doc\\FPIBGSprint001.md")
bc.Open()
bc.Close()

bc = pptimg2md("X:\\doc\\FPIBGProjectTOC","X:\\doc\\FPIBGProjectTOC.md")
bc.Open()
bc.Close()
