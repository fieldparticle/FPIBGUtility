import sys

syspth = sys.path
sys.path.append("x:\\SPRINT002MOD003\\FPIBGUtility\\python\\shared")
'''Demonstrates triple double quotes
    docstrings and does nothing really.'''
from FPIBGclient import TCPIP
client = TCPIP()
client.openConnection()
client.writeData("Particle.cfg")
