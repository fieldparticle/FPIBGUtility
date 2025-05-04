from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from gpu_ParticleSystem import *
from gpu_CollImage import *
from subprocess import call

from gpu_plotParticle import *

class GPUStudies(ParticleSystem):

    def __init__(self):
        super().__init__()

    def Create(self):
        numParts = 2
        Xlen = 2
        YLen = 2
        ZLen = 2
        #coll = CollImg(10,10,10)
        self.setTimeStep(0.01)

        self.addParm(1.0,100,[1.0,1.5,1.5],[1.0,0.0,0.0],0.25)
        self[0].setColor((0.1, 0.2, 0.5))

        self.addParm(1.0,150,[2.0,1.5,1.5],[-1.0,0.0,0.0],0.25)
        self[0].setColor((0.6, 0.2, 0.5))
        self.setEndFrame(20)
        
