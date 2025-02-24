import sys
import os
syspth = sys.path
os.chdir("..\\")
sys.path.append("X:\\SPRINT002MOD003\\FPIBGUtility\\python\\shared")
'''Demonstrates triple double quotes
    docstrings and does nothing really.'''
from FPIBGclient import TCPIP
client = TCPIP()
client.openConnection()
client.writeData("Particle.cfg")

