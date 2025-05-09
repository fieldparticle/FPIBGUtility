from dataclasses import dataclass,field
from typing import List,ClassVar
import threading
from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from gpu_plotParticle import *
from ps_ParticleSystem import *
from gpu_LockCellArray import *
from subprocess import call

from gpu_utility import *
import atomics

# importing numpy 
import numpy as np 

class Particle:

	
    def __init__(self):
        self.maxoccp = 8
        self.dt = 0
        self.pnum =0
        self.colFlg = 0
        self.MolarMatter =0.0
        self.temp_vel = 0.0
        self.PosLoc =  [0.0,0.0,0.0,0.0]
        self.VelRad = [0.0,0.0,0.0,0.0]
        self.prvvel = [0.0,0.0,0.0,0.0]
        self.parms = [0.0,0.0,0.0,0.0]
        self.zlink = [int]*self.maxoccp
        self.bcs =  [int]*4
        self.ccs = [int,int]*12
        self.color = (0.0, 0.0, 0.0)
        self.particleDead = False
        self.initalPosition = [0.0,0.0,0.0,0.0]
        self.rptVelPos= False
        self.svCellAry = False
        self.rptVel = False
        self.ups_i1 = []
        self.ups_i2 = []
        self.rptIntersectionPoints=False
        self.pltVelVec = False
        self.velAngr = 0.0
        self.velAngd = 0.0

    from ps_particleIntersection import particlesIntersection

    def plotVelVec(self,flag):
        self.pltVelVec = flag

    def setColor(self,color):
        self.color = color
	
    def reportVelPos(self,flag):
        self.rptVelPos = flag

    def reportIntersectionPoints(self,flag):
        self.rptIntersectionPoints = flag

    def changePos(self, delVel,dt):
        self.PosLoc[0] = self.PosLoc[0]+self.VelRad[0]*dt
        self.PosLoc[1] = self.PosLoc[1]+self.VelRad[1]*dt
        self.PosLoc[2] = self.PosLoc[2]+self.VelRad[2]*dt

        if(self.rptVelPos == True):
            print("P:",self.pnum," loc:",self.PosLoc," vel:",self.VelRad)
            
		
    def plotVelocityVector(self):
        #self.velAngr = calcAtan2(self.VelRad[0],self.VelRad[1])
        self.velAngr = math.atan2(self.VelRad[1],self.VelRad[0])
        self.velAngd = self.velAngr*180/math.pi
        
        tx = self.PosLoc[0]+self.PosLoc[3]*math.cos(self.velAngr)
        ty = self.PosLoc[1]+self.PosLoc[3]*math.sin(self.velAngr) 
        x,y = [ self.PosLoc[0],tx], [self.PosLoc[1] ,ty ]
        
        print("velvec angr:{}, angd:{}, vel:<{},{}> sin(ang):{} cos:{}, p:{},ang:{:.4f} from <{:.4f},{:.4f}> to <{:.4f},{:.4f}>".format(self.velAngr, 
                                                                                                                                    self.velAngd,
                                                                                                                                    self.VelRad[0],
                                                                                                                                    self.VelRad[1],
                                                                                                                                    math.cos(self.velAngr),
                                                                                                                                    math.sin(self.velAngr),
                                                                                                                                    self.pnum,self.velAngd,
                                                                                                                                     self.PosLoc[0],self.PosLoc[1],tx,ty))
        R = [ [math.cos(self.velAngr), -math.sin(self.velAngr)],[math.sin(self.velAngr),math.cos(self.velAngr)] ]

        return x,y


    def reportVelocity(self,flag):
        self.rptVel == flag

