from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from ps_ParticleSystem import *
from gpu_LockCellArray import *
from subprocess import call

from gpu_plotParticle import *

class GPUStudies(ParticleSystem):

    def __init__(self):
        super().__init__()

    def Create(self):
        calcAtan2()
        self.desc = "This performs a collision between two particle along the x axis."
        self.code = "2PTHorzCollisionTest"
        numParts = 2
        Xlen = 2
        YLen = 2
        ZLen = 2
        #coll = CollImg(10,10,10)
        self.SetWHD(20,10,1,10)
        # Time step for velocity
        self.setTimeStep(0.01)
        # Frame rate
        self.setFrameRate(200)
        self.addParm(1.0,100,[1.0,1.5,1.5],[1.0,0.0,0.0],0.25)
        self[0].setColor((255, 0, 0))
        self[0].reportVelPos(False)
        self[0].reportVelocity(False)
        self[0].reportIntersectionPoints(True)
        

        self.addParm(1.0,150,[2.0,1.5,1.5],[-1.0,0.0,0.0],0.25)
        self[1].setColor((0,0,255))
        self[1].reportVelPos(False)
        self[1].reportVelocity(False)
        self[1].reportIntersectionPoints(True)
	

        self.setEndFrame(30)
        self.setSaveCellArrayFrames([1,2])
        self.saveCellArray(True)
        self.reportDups(False)
        self.reportAtomic(False)
        self.reportCells(False)
        self.reportFrame(False)
        self.reportCollison(False)

    def reset(self):
        for ii in range(len(self)):
            self[ii].PosLoc = self[ii].initalPosition


        


        
