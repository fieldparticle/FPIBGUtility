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

    substName    =  0.0
    molar_matter =  0.0
    matter       =  0.0
    radius       =  0.0
    R            =  0.0
    vap_temp     =  0.0
    avgdr        = 6.022E23     # Avagrado 1/mol
    k_B          = 1.380649E-23 # Boltzman Constant J/K 
    maxvel       = 0.0
    minvel       = 0.0
    vel_vap      = 0.0
    velRange     = 0.0
    f_repulse    = 0.0
    f_attract    = 0.0
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
        self.pltIntersectVec = False
        self.pltOrientVec = False
        self.ovec = []
        self.rptOrientVec = False
        self.phi = 0.0
        self.pltProxVec = False
        self.rptProxVec =False
        self.velvecx = []
        self.velvecy =[]
        self.isec1 = []
        self.isec2 = []
        self.prxVec = []
        self.prxVecx = []
        self.prxVecy = []
        self.lowTemp = 0.0
        self.highTemp = 0.0

    from ps_particleIntersection import particlesIntersection
    from ps_calcOrientVec import calcOrientVec
    from ps_calcProximityVec import calcProximityVec
    from ps_CalcVelVec import calcVelocityVector

    def setTempRange(self,sysTemp,low,high):
        self.sysTemp   = sysTemp
        self.lowTemp = low
        self.highTemp = high


    def repotProxVec(self,flag):
        self.rptProxVec = flag

    def plotProxVec(self,flag):
        self.pltProxVec = flag
    
    def plotIntersectVec(self,flag):
        self.pltIntersectVec = flag
        
    def plotOrientVec(self,flag):
        self.pltOrientVec = flag

    def repotOrientVec(self,flag):
        self.rptOrientVec = flag
        

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
            
    def reportVelocity(self,flag):
        self.rptVel == flag

    def calcAttraction(self,temp):
        f_attract = math.sqrt((3*self.R*self.vap_temp)/self.molar_matter)/self.velRange
        return f_attract
    
    def calcRepulsion(self,temp):
        vel = self.calcTempVelocity(temp)
        f_repulse = vel/self.dt
        f_repulse = f_repulse/self.velRange 
        return f_repulse

    def calcTempVelocity(self,temp):
        vel = math.sqrt((3*self.R*temp)/self.molar_matter)
        vel = vel/self.velRange
        return vel
    
    def setSubstance(self,Name,MolarMass,AtomicRadius,R,VapTemp):
        self.substName    = Name
        self.molar_matter = MolarMass
        self.matter       = MolarMass/self.avgdr
        self.radius       = AtomicRadius
        self.R            = R
        self.vap_temp     = VapTemp
        # Root mean square speed - https://en.wikipedia.org/wiki/Maxwell%E2%80%93Boltzmann_distribution
        self.maxvel       = math.sqrt((3*self.R*self.highTemp)/self.molar_matter) 
        self.minvel       = math.sqrt((3*self.R*self.lowTemp)/self.molar_matter) 
        # velocity range to normaize velocity
        self.velRange     = self.maxvel-self.minvel
        # This is the attraction velocity which occurs at the fluid/vapor boundary
        self.vel_vap      = math.sqrt((3*self.R*self.vap_temp)/self.molar_matter)/self.velRange
        
        