###############################################################
## Preamble to every script. Will append the shared directory #
import sys                                                    #  
import os                                                     #
syspth = sys.path                                             #
cwd = os.getcwd()                                             #
shrddir = cwd + "\\python\\shared"  
sys.path.append(shrddir)           
shrddir = cwd + "\\python\\unittest"  
sys.path.append(shrddir)           
import getpass                                                #
print(getpass.getuser())                                      #
guser = getpass.getuser()                            #
# Now do imports                                              #
###############################################################
from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from gpu_ParticleSystem import *
from gpu_CollImage import *
from subprocess import call
from test_Indexing import *
from gpu_plotParticle import *

numParts = 2
Xlen = 2
YLen = 2
ZLen = 2
#particle = Particle()
#print(particle)
#print(particle.PosLoc)
#print(particle.zlink)
#print(particle.ccs)
#print(particle.bcs)
coll = CollImg(10,10,10)
#print(coll)
#print(coll.collImg)

ps = ParticleSystem()
ps.setTimeStep(0.01)

ps.addParm(1.0,100,[1.0,1.5,1.5],[1.0,0.0,0.0],0.25)
ps[0].setColor((0.1, 0.2, 0.5))

ps.addParm(1.0,150,[2.0,1.5,1.5],[-1.0,0.0,0.0],0.25)
ps[0].setColor((0.6, 0.2, 0.5))
ps.setEndFrame(20)
ps.run()


"""
ps = ParticleSystem(numParts)
for ii in range(numParts):
    particleList.add(Particle())
"""


"""
ps.print()
ps.setEndFrame(10)
ps.run()
"""



if False:
    os.chdir(cwd)
    call(["pytest","python/unittest/test_Indexing.py","-s"]) 
    from test_Indexing import *

