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
        self.desc = "This performs a collision between two particle along the x axis."
        self.code = "2PTHorzCollisionTest"
        numParts = 2
        Xlen = 2
        YLen = 2
        ZLen = 2
        #coll = CollImg(10,10,10)
        self.setTimeStep(0.001)

        self.addParm(1.0,100,[1.0,1.5,1.5],[1.0,0.0,0.0],0.25)
        self[0].setColor((255, 0, 0))

        self.addParm(1.0,150,[2.0,1.5,1.5],[-1.0,0.0,0.0],0.25)
        self[1].setColor((0,0,255))
        self.setEndFrame(20)
        self.SetWHD(10,10,10,3)

    def reset(self):
        self[0].PosLoc[0] = 1.0
        self[0].PosLoc[1] = 1.5
        self[0].PosLoc[2] = 1.5

        self[1].PosLoc[0] = 2.0
        self[1].PosLoc[1] = 1.5
        self[1].PosLoc[2] = 1.5



        
