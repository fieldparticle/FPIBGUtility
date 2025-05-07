from dataclasses import dataclass,field
from typing import List,ClassVar
import threading
from gpu_plotParticle import *
from gpu_compute import *
from gpu_vertex import *
from gpu_graphics import *
from ps_ParticleSystem import *
from gpu_LockCellArray import *
from subprocess import call
from gpu_plotParticle import *
from gpu_utility import *
from gpu_particle import *
import atomics


# importing numpy 
import numpy as np 
	
class ParticleSystem(List) :
    	
	totParts 	= 0
	delt 		= 0.0
	endFrame 	= 100
	width 		= 0
	height 		= 0 
	depth 		= 0
	max_ocup	= 0
	frameNum 	= 0        
	rptCells	= False
	rptFrame	= False
	frameRate   = 1000
	count 		= 0
	frames 		= []
	rptCollison = False
	def __init__ (self):
		super().__init__(self)
		#self.plotParts = ParticlePlot2D(self)
		self.rdups = False
		#Add a particle 0
		self.addParm(0,0,[0,0,0],[0,0,0],0)


	def setFrameRate(self,fr):
		self.frameRate = fr

	def setTimeStep(self,delt):
		self.dt= delt

	def reportCollison(self,flag):
		self.rptCollison = flag

	def reportAtomic(self,flag):
		self.lockindex.reportAtomic(flag)

	def reportFrame(self,flag):
		self.rptFrame = flag

	def frameReset(self):
		self.cellAry.reset()
		self.lockindex.reset()
		
	def SetWHD(self,width,height,depth,max_ocup):
		self.max_ocup = max_ocup
		self.width = width
		self.height = height
		self.depth = depth
		self.cellAry = CellArray(self.width,self.height,self.depth,self.max_ocup)
		self.lockindex = LockIndex(self.width,self.height,self.depth)

	def writeCellArray(self,frameNum):
		if frameNum in self.frames:
			self.cellAry.writeCellArray(frameNum)

	def saveCellArray(self,flag):
		self.svCellAry = flag
	
	def setSaveCellArrayFrames(self,frames):
		self.frames = frames

	def reportCells(self,flag):
		self.rptCells = flag

	def reportDups(self,flag):
		self.rdups = flag

	def setEndFrame(self,endFrame):
		self.endFrame = endFrame

	def addParm(self,matter,temp_vel,posary,velary,radius):
		particle = []
		particle = Particle()
		particle.pnum = self.totParts
		particle.temp_vel = temp_vel
		particle.PosLoc[0] = posary[0]
		particle.PosLoc[1] = posary[1]
		particle.PosLoc[2] = posary[2]
		particle.PosLoc[3] = radius
		particle.initalPosition = particle.PosLoc
		particle.VelRad[0] = velary[0]
		particle.VelRad[1] = velary[1]
		particle.VelRad[2] = velary[2]
		self.append(particle)
		self.totParts  = len(self)
	
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
	
		maxloc = self.width*self.height*self.depth
		#ArrayToIndex(locary,width,height,maxLocation):

		self[pnum].zlink[0] = ArrayToIndex([round(cx+R),round(cy+R),round(cz-R)],self.width,self.height,maxloc)
		if self[pnum].zlink[0] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))
		
		self[pnum].zlink[1] = ArrayToIndex([round(cx+R),round(cy+R),round(cz+R)],self.width,self.height,maxloc)
		if self[pnum].zlink[1] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
			
		self[pnum].zlink[2] = ArrayToIndex([round(cx-R),round(cy+R),round(cz+R)],self.width,self.height,maxloc)
		if self[pnum].zlink[2] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[3] = ArrayToIndex([round(cx-R),round(cy+R),round(cz-R)],self.width,self.height,maxloc)
		if self[pnum].zlink[3] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[4] = ArrayToIndex([round(cx+R),round(cy-R),round(cz+R)],self.width,self.height,maxloc)
		if self[pnum].zlink[4] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[5] = ArrayToIndex([round(cx+R),round(cy-R),round(cz-R)],self.width,self.height,maxloc)
		if self[pnum].zlink[5] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
		
		self[pnum].zlink[6] = ArrayToIndex([round(cx-R),round(cy-R),round(cz+R)],self.width,self.height,maxloc)
		if self[pnum].zlink[6] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	

		self[pnum].zlink[7] = ArrayToIndex([round(cx-R),round(cy-R),round(cz-R)],self.width,self.height,maxloc)
		if self[pnum].zlink[7] == 0:
			print("Particle Corner:{} missed <{}{}{}".format(pnum,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))	
	
	def removeCornerDups(self,pnum):
		kk = 0
		for ii in range(8):
			for jj  in range(8):
				if jj != ii:
					if self[pnum].zlink[ii] == self[pnum].zlink[jj]:
						if(self.frameNum == 1):
							if self.rdups == True:
								print("Frame:{} dup for p{}: at {}".format(self.frameNum,pnum,self[pnum].zlink[ii]))
						self[pnum].zlink[jj]= 0
				else:
					kk += 1
		if self.rdups == True:
			print(self[pnum].zlink)

	def locateCorners(self,pnum):
		
		for ii in range(8):
			sltidx = 0
			slot 	= 0
			sltidx = self[pnum].zlink[ii]
		
			if sltidx != 0:
				slot = self.lockindex.atomicAdd(sltidx)-1
				if slot >= self.cellAry.maxOccupancy:
					print("VERT slot exceeds number of cells   F:{},P:{},sltidx:{}, slot:{}".format(
						self.frameNum,pnum,self[pnum].PosLoc[3],sltidx,slot))
					
					return 1
				
				if sltidx >= self.cellAry.size:
					print("VERT slot index exceed number of allowed cell occupants   F:{},P:{},R:{},sltidx:{}, slot:{} at loc: {}({},{},{})".format(
						self.frameNum,pnum,self[pnum].PosLoc[3],sltidx,slot,self[pnum].PosLoc[0],self[pnum].PosLoc[1],self[pnum].PosLoc[2]))
					return 1
				
				if(self.rptCells == True):
					print("VERT F:{} added P{} Corner:{} to cellAry sltidx:{} and occup slot:{}".format(self.frameNum,pnum,ii,sltidx,slot))
		  

				self.cellAry.loc[sltidx][slot] = pnum
		return 0
		
	def processVertex(self,pnum):
		if(pnum == 0):
			return
		if self[pnum].particleDead == True:
			return
		# Process corners
		self[pnum].changePos([0.1,0.0,0.0],self.dt)
		self.getCornerIndexes(pnum)
		self.removeCornerDups(pnum)
		if self.locateCorners(pnum) > 0:
			self[pnum].particleDead = True
		
		
	def processCompute(self,pnum):
		if(pnum == 0):
			return
		duplst = []
		dupflg = False
		for ii in range(8):
	
			# Set location to local variable.
			loc =self[pnum].zlink[ii]
			# If the lcation is not zero..
			if (loc != 0):
				# Use the linked particle location to index into the particle-cell hash table 
				# And compare this particle with all of the paricles at this location.
				for jj in range(self.cellAry.maxOccupancy):
				
					Tindex = self.cellAry.loc[loc][jj]
					
					if(Tindex == 0 ):
						break
						
					if jj == 0:
						duplst.append(Tindex)
					else:
						#----------------------- DUP Process start		
						for cc in range(len(duplst)):
							if(duplst[cc] == Tindex):
								dupflg = True
								break
					
							if(duplst[cc] == 0):
								dupflg = False
								duplst.append(Tindex)
								break
			
					if(dupflg == False):
						if(self.isParticleContact(pnum, Tindex) == True):
							self[pnum].particlesIntersection(self[pnum],self[Tindex])
							dupflg = True

	def isParticleContact(self,pnum, opnum):

		if(pnum == opnum):
			return False
		
		if(self.rptCollison == True):
			txt = "Comparing Particle {} with particle {}".format(pnum,opnum)
			print(txt)
	
		xT = self[pnum].PosLoc[0]
		yT = self[pnum].PosLoc[1]
		zT = self[pnum].PosLoc[2]

		xP = self[opnum].PosLoc[0]
		yP = self[opnum].PosLoc[1]
		zP = self[opnum].PosLoc[2]

		
		 # Get distance between centers
		dsq = ((xP-xT)*(xP-xT)+
					(yP-yT)*(yP-yT)+
					(zP-zT)*(zP-zT))
		rsq = (self[pnum].PosLoc[3]+self[opnum].PosLoc[3])*(self[pnum].PosLoc[3]+self[opnum].PosLoc[3])

		rddiff = dsq-rsq;	
		
		if rddiff < 0.0001:
			self[pnum].colFlg = True
			if(self.rptCollison == True):
				txt = "Collion Particle {} with particle {}".format(pnum,opnum)
				print(txt)
			return True
		
		return False
		
	def getEndFrame(self):
		return self.endFrame
		
	def update(self):
		#print("Frame:",tt)
		for ii in range(self.totParts):
			t =threading.Thread(target=self.processVertex,args=(ii,))
			t.start()
			t.join()
	 	
		if self.svCellAry == True:
			self.writeCellArray(self.frameNum)

		for ii in range(self.totParts):
			t =threading.Thread(target=self.processCompute,args=(ii,))
			t.start()
			t.join()
	 		
		self.frameReset()

		
		#print("Thread {} complete.".format(ii))

		

	def print(self):
		for ii in self:
			print("==============\r")
			print(ii.pnum,"\r")
			print(ii.colFlg,"\r")
			print(ii.MolarMatter,"\r")
			print(ii.temp_vel,"\r")
			print(ii.PosLoc,"\r")
			print(ii.VelRad,"\r")
			