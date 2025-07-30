from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from ps_ParticleSystem import *
from gpu_LockCellArray import *
from subprocess import call
import numpy as np
from gpu_plotParticle import *

class SubsProp(ParticleSystem):

    def __init__(self):
        super().__init__()
        self.testAngle = np.linspace( 0 , 2 * np.pi , 150 )

    def Create(self):
        
        self.desc = "Plot subsance properties temperature velocity, acceleration, repulsion."
        self.code = "SubsProp"
        numParts = 2
        Xlen = 2
        YLen = 2
        ZLen = 2
        
        self.SetWHD(20,10,1,10)
        # Time step for velocity
        self.setTimeStep(0.01)
        # Frame rate
        self.setFrameRate(200)
        self.addParm(1.0,100,[1.20,1.5,1.5],[1.0,0.0,0.0],0.25)
        self[1].setTempRange(250,1,400)
        self[1].setSubstance("He",4.0026022,28,8.3145,-268.9+273.15)
        self[1].setColor((255, 0, 0))
        self[1].reportVelPos(False)
        self[1].reportVelocity(False)
        self[1].reportIntersectionPoints(False)
        self[1].repotOrientVec(True)
        self[1].repotProxVec(True)

        self[1].plotVelVec(False)
        self[1].plotIntersectVec(False)
        self[1].plotOrientVec(True)
        self[1].plotProxVec(True)

    def reset(self):
        for ii in range(len(self)):
            self[ii].PosLoc = self[ii].initalPosition

    def processVertex(self,pnum):
        self[pnum].colFlg = True
        if(pnum == 0):
            return

        if(pnum == 1):
            self[pnum].particlesIntersection(self[1],self[2])

        if(pnum == 2):
            self[pnum].particlesIntersection(self[2],self[1])
           
        self[pnum].calcOrientVec()
        self[pnum].calcProximityVec()

        if pnum == 2:
            self.rotateParticle(2)

        
    def rotateParticle(self,pnum):
        i = self.testAngle[self.frameNum]
        self[2].PosLoc[0] = self[1].PosLoc[0]+1.25*math.cos(i)*self[1].PosLoc[3] 
        self[2].PosLoc[1] = self[1].PosLoc[1]+1.25*math.sin(i)*self[1].PosLoc[3] 
        self.velTestAngle = i
        print(i)

    def processCompute(self,pnum):
        pass
