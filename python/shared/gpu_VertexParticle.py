from dataclasses import dataclass,field
from typing import List,ClassVar

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


	
class VertexParticle(List) :
    	
	totParts = 0
	def __init__ (self):
		super().__init__(self)

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


	def print(self):
		for ii in self:
			print("==============\r")
			print(ii.pnum,"\r")
			print(ii.colFlg,"\r")
			print(ii.MolarMatter,"\r")
			print(ii.temp_vel,"\r")
			print(ii.PosLoc,"\r")
			print(ii.VelRad,"\r")
			