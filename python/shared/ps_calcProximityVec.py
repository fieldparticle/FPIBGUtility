from gpu_utility import *
import math
import numpy as np 

def calcProximityVec(self):
    A = np.array(self.opos[0]-self.PosLoc[0])
    B = np.array(self.opos[1]-self.PosLoc[1])
    c = np.linalg.norm(A-B)
    c = math.sqrt((self.opos[0]-self.PosLoc[0])**2+(self.opos[1]-self.PosLoc[1])**2)
    self.seplen = abs(self.PosLoc[3]-c)
    self.proxlen = abs(self.PosLoc[3]-2.0*self.seplen)
    self.phi = (self.seplen)/self.PosLoc[3] 
    self.prxVecx= self.PosLoc[0]+self.proxlen*math.cos(self.angOrt)
    self.prxVecy= self.PosLoc[1]+self.proxlen*math.sin(self.angOrt)


    if self.rptProxVec == True:
        print("Phi:{:.4f},orxlen:{:.4f},angOrnt:{:0.4f},seplen:{:.4f},proxlen:{:.4f},prxVec:<{:.4f},{:.4f}>".format(
            self.phi,
            c,
            self.angOrt,
            self.seplen,
            self.proxlen,
            self.prxVecx,
            self.prxVecy))
