import array
from gpu_utility import *
def calcOrientVec(self):
    p1 = np.array(self.ups_i1)
    p2 = np.array(self.ups_i2)
    self.opos = (p1+p2)/2.0
    self.ortVecx = self.opos[0]
    self.ortVecy = self.opos[1]
    self.oposx =  self.opos[0].item()
    self.oposy =  self.opos[1].item()
    self.ortVec =  np.asarray([self.opos[0],self.opos[1]])
    self.angOrt = atan2o(self.opos[0]-self.PosLoc[0],self.opos[1]-self.PosLoc[1])
    angOrtd =  math.degrees(self.angOrt)

    if self.rptOrientVec == True:
        print("opos:<{:.4f},{:.4f}>, angOrt:{:.4f},ortVec:<{:.4f},{:.4f},{:.4f},{:.4f}>".format(
            self.opos[0],self.opos[1],angOrtd,self.PosLoc[0],self.PosLoc[1],self.opos[0],self.opos[1]))
        
