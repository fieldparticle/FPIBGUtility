from dataclasses import dataclass,field
from typing import List,ClassVar
import threading
from gpu_plotParticle import *

# importing numpy 
import numpy as np 

@dataclass
class lstr:
    pindex : int=0
    ploc : int=0
    fill : int =0

@dataclass
class bcoll: 
	clflg : int = 0
	
@dataclass
class ccoll :
	pindex : int = 0
	clflg : int = 0 

def allocListlstr(list):
	for x in range(len):
		LSTR = lstr()
		list.zlink.append(LSTR)


class Particle:

	def __init__(self):
		self.dt = 0
		self.pnum =0
		self.colFlg =0
		self.MolarMatter =0.0
		self.temp_vel = 0.0
		self.PosLoc =  [0.0,0.0,0.0,0.0]
		self.VelRad = [0.0,0.0,0.0,0.0]
		self.prvvel = [0.0,0.0,0.0,0.0]
		self.parms = [0.0,0.0,0.0,0.0]
		self.zlink = [int,int,int]*8
		self.bcs =  [int]*4
		self.ccs = [int,int]*12
		self.color = (0.0, 0.0, 0.0)
		
	def setColor(self,color):
		self.color = color
		pass

	def changePos(self, delVel,dt):
		#self.VelRad[0] = self.VelRad[0] + delVel[0]
		#self.VelRad[1] = self.VelRad[1] + delVel[1]
		#self.VelRad[2] = self.VelRad[2] + delVel[2]

		self.PosLoc[0] = self.PosLoc[0]+self.VelRad[0]*dt
		self.PosLoc[1] = self.PosLoc[1]+self.VelRad[1]*dt
		self.PosLoc[2] = self.PosLoc[2]+self.VelRad[2]*dt
		if(self.pnum == 2):
			print("P:",self.pnum," loc:",self.PosLoc," vel:",self.VelRad)
			
		



	
class ParticleSystem(List) :
    	
	totParts = 0
	delt = 0.0
	endFrame = 100
	
	def __init__ (self):
		super().__init__(self)
		self.plotParts = ParticlePlot2D(self)

	def setTimeStep(self,delt):
		self.dt= delt

	def setEndFrame(self,endFrame):
		self.endFrame = endFrame

	def addParm(self,matter,temp_vel,posary,velary,radius):
		particle = []
		particle = Particle()
		self.totParts += 1
		particle.pnum = self.totParts
		particle.temp_vel = temp_vel
		particle.PosLoc[0] = posary[0]
		particle.PosLoc[1] = posary[1]
		particle.PosLoc[2] = posary[2]
		particle.PosLoc[3] = radius
		particle.VelRad[0] = velary[0]
		particle.VelRad[1] = velary[1]
		particle.VelRad[2] = velary[2]
		self.append(particle)
		
	def add(self,part):
		part.pnum = self.totParts
		self.append(part)


	def processVertex(self,pnum):
		self[pnum].changePos([0.1,0.0,0.0],self.dt)
		

	def run(self):
		self.plotParts.start()
		self.update()

		
	def update(self):
		for tt in range(self.endFrame):
			#print("Frame:",tt)
			for ii in range(self.totParts):
				t =threading.Thread(target=self.processVertex,args=(ii,))
				t.start()
				t.join()
			self.plotParts.plotParticle()
		

	def print(self):
		for ii in self:
			print("==============\r")
			print(ii.pnum,"\r")
			print(ii.colFlg,"\r")
			print(ii.MolarMatter,"\r")
			print(ii.temp_vel,"\r")
			print(ii.PosLoc,"\r")
			print(ii.VelRad,"\r")
			