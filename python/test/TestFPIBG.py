
#############################################################################################
## Preamble to every script. Will append the shared directory                               #
import sys                                                                                  #  
import os                                                                                   #
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared'))) 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../unittest')))   #
import getpass                                                                              #
print(getpass.getuser())                                                                    #
guser = getpass.getuser()   
cwd = os.getcwd()#    
print(cwd)
# Now do imports                                                                            #
#############################################################################################
from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from gpu_VertexParticle import *
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

particleList = VertexParticle()

particleList.addParm(1.0,100,[1.0,1.5,1.5],[1.0,0.0,0.0],0.25)
particleList.addParm(1.0,150,[2.0,1.5,1.5],[-1.0,0.0,0.0],0.25)



#        particleList = VertexParticle(numParts)
#        for ii in range(numParts):
#            particleList.add(Particle())

particleList.print()
p = ParticlePlot(particleList)
p.viewXY()
p.plotSphere()
if False:
    os.chdir(cwd)
    call(["pytest","python/unittest/test_Indexing.py","-s"]) 
    from test_Indexing import *

