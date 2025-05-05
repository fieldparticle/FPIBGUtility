from dataclasses import dataclass,field
from typing import List,ClassVar
import threading
from gpu_plotParticle import *
from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from gpu_ParticleSystem import *
from gpu_CollImage import *
from subprocess import call
from gpu_plotParticle import *
from gpu_utility import *
import atomics


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
		self.maxoccp = 8
		self.dt = 0
		self.pnum =0
		self.colFlg =0
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
		"""
		if(self.pnum == 2):
			print("P:",self.pnum," loc:",self.PosLoc," vel:",self.VelRad)
		"""	
		



	
class ParticleSystem(List) :
    	
	totParts 	= 0
	delt 		= 0.0
	endFrame 	= 100
	width 		= 0
	height 		= 0 
	depth 		= 0
	max_ocup	= 0
	frameNum 		= 0        
	def __init__ (self):
		super().__init__(self)
		self.plotParts = ParticlePlot2D(self)
		
	def setTimeStep(self,delt):
		self.dt= delt

	def SetWHD(self,width,height,depth,max_ocup):
		self.max_ocup = max_ocup
		self.width = width
		self.height = height
		self.depth = depth
		self.collImg = CollImg(self.width,self.height,self.depth,self.max_ocup)
		self.lockindex = LockIndex(self.width,self.height,self.depth)


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
	
	def incFrame(self):
		self.frameNum += 1
	
	
	def add(self,part):
		part.pnum = self.totParts
		self.append(part)

	def getCornerIndexes(self,pnum):
		cx 		= self[pnum].PosLoc[0]
		cy 		= self[pnum].PosLoc[1]
		cz 		= self[pnum].PosLoc[2]
		R		= self[pnum].PosLoc[3]
	
		#ArrayToIndex(locary,width,height,maxLocation):

		self[pnum].zlink[0] = ArrayToIndex([round(cx+R),round(cy+R),round(cz-R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[0] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))
		
		self[pnum].zlink[1] = ArrayToIndex([round(cx+R),round(cy+R),round(cz+R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[1] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
			
		self[pnum].zlink[2] = ArrayToIndex([round(cx-R),round(cy+R),round(cz+R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[2] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[3] = ArrayToIndex([round(cx-R),round(cy+R),round(cz-R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[3] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[4] = ArrayToIndex([round(cx+R),round(cy-R),round(cz+R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[4] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[5] = ArrayToIndex([round(cx+R),round(cy-R),round(cz-R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[5] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[6] = ArrayToIndex([round(cx-R),round(cy-R),round(cz+R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[6] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	

		self[pnum].zlink[7] = ArrayToIndex([round(cx-R),round(cy-R),round(cz-R)],self.width,self.height,self.width*self.height*self.depth)
		if self[pnum].zlink[7] == 0:
			print("Particle:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
	
	def removeCornerDups(self,pnum):
		kk = 0
		for ii in range(8):
			for jj  in range(8):
				if jj != ii:
					if self[pnum].zlink[ii] == self[pnum].zlink[jj]:
						if(self.frameNum == 1):
							print("Frame:{} dup for p{}: at {}".format(self.frameNum,pnum,self[pnum].zlink[ii]))
						self[pnum].zlink[jj]= 0
				else:
					kk += 1
						
	def locateCorners(self,pnum):
		for ii in range(8):
			sltidx = 0
			slot 	= 0
			sltidx = self[pnum].zlink[ii]
		
			if sltidx != 0:
				slot = self.lockindex[sltidx].fetch_inc()
				if slot >= self.lockindex.size(): 
					print("VERT slot>MAX_ARY  F:{},P:{},R:{},Slots:{},at loc: {}({},{},{}), exceeds max array:{}".format(
						self.frameNum),pnum,self[pnum].PosLoc[3],8,sltidx,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2],slot)
					
				self.collImg[sltidx][slot] = pnum
		
	def processVertex(self,pnum):
		# Process corners
		self[pnum].changePos([0.1,0.0,0.0],self.dt)
		self.getCornerIndexes(pnum)
		self.removeCornerDups(pnum)
		self.locateCorners(pnum)
		
		

	def run(self):
		self.plotParts.start()
		self.update()

	def getEndFrame(self):
		return self.endFrame
		
	def update(self):
		for tt in range(self.endFrame):
			#print("Frame:",tt)
			for ii in range(self.totParts):
				t =threading.Thread(target=self.processVertex,args=(ii,))
				t.start()
				t.join()

		

	def print(self):
		for ii in self:
			print("==============\r")
			print(ii.pnum,"\r")
			print(ii.colFlg,"\r")
			print(ii.MolarMatter,"\r")
			print(ii.temp_vel,"\r")
			print(ii.PosLoc,"\r")
			print(ii.VelRad,"\r")
			