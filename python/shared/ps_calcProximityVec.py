
import math
import numpy as np 

def calcProximityVec(self):
    A = np.array(self.ortVecx)
    B = np.array(self.ortVecy)
    c = np.linalg.norm(A-B)
    self.proxlen = self.PosLoc[3]-c
    self.phi = (self.proxlen)/self.PosLoc[3] 
    
    if self.rptProxVec == True:
        print("Phi:{:0.4f},proxlen:{:0.4f},isec1:<{},{}>,isec2:<{},{}>".format(self.phi,self.proxlen,self.ups_i1[0],self.ups_i1[1],self.ups_i2[0],self.ups_i2[1]))
