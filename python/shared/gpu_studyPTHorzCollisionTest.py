from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from ps_ParticleSystem import *
from gpu_LockCellArray import *
from subprocess import call

from gpu_plotParticle import *

class PTHorzCollisionTest(ParticleSystem):

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
        self.SetWHD(20,10,1,10)
        # Time step for velocity
        self.setTimeStep(0.01)
        # Frame rate
        self.setFrameRate(200)
        self.addParm(1.0,100,[1.20,1.5,1.5],[1.0,0.0,0.0],0.25)
        self[1].setTempRange(250,1,400)
        self[1].setSubstance("He",4.0026022,28,8.3145,-268.9+273.15)
        self[1].setColor((255, 0, 0))
        self[1].reportVelPos(True)
        self[1].reportVelocity(True)
        self[1].reportIntersectionPoints(False)
        self[1].repotOrientVec(False)
        self[1].repotProxVec(False)


        self[1].plotVelVec(True)
        self[1].plotIntersectVec(True)
        self[1].plotOrientVec(True)
        self[1].plotProxVec(True)

    
        self.addParm(1.0,150,[1.80,1.5,1.5],[-1.0,0.0,0.0],0.25)
        self[2].setTempRange(250,1,400)
        self[2].setSubstance("He",4.0026022,28,8.3145,-268.9+273.15)
        self[2].setColor((0,0,255))
        self[2].reportVelPos(True)
        self[2].reportVelocity(True)
        self[2].reportIntersectionPoints(False)
        self[2].repotOrientVec(False)
        self[2].repotProxVec(False)

        self[2].plotIntersectVec(False)
        self[2].plotVelVec(True)
        self[2].plotOrientVec(False)
        self[2].plotProxVec(False)

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

    def processVertex(self,pnum):
        if(pnum == 0):
            return
        if self[pnum].particleDead == True:
            return
        # Process corners
        self[pnum].changePos([0.1,0.0,0.0],self.dt)
        self[pnum].calcVelocityVector()
        self.getCornerIndexes(pnum)
        self.removeCornerDups(pnum)
        if self.locateCorners(pnum) > 0:
            self[pnum].particleDead = True
        
        
        
    def processCompute(self,pnum):
        self.processComputeItem(pnum)
