import array
from gpu_utility import *
def calcOrientVec(self):
    p1 = np.array(self.ups_i1)
    p2 = np.array(self.ups_i2)
    self.opos = (p1+p2)/2
    self.ortVecx = [self.PosLoc[0],self.opos[0]]
    self.ortVecy = [self.PosLoc[0],self.opos[1]]
    self.oposx =  self.opos[0].item()
    self.oposy =  self.opos[1].item()
    self.ortVec =  np.asarray([self.opos[0],self.opos[1]])

    if self.rptOrientVec == True:
        print("opos:<{:.4f}{:.4f}>, ortVec:<{:.4f},{:.4f},{:.4f},{:.4f}>".format(self.opos[0],self.opos[1],self.PosLoc[0],self.PosLoc[1],self.opos[0],self.opos[1]))
        
