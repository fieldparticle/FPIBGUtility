import math
import numpy as np 
from gpu_utility import *
import array
def calcVelocityVector(self):
    self.velAngr = atan2o(self.VelRad[0],self.VelRad[1])
    self.velAngd = self.velAngr*180/math.pi
    self.velvecx = [self.PosLoc[0],self.PosLoc[0]+self.PosLoc[3]*math.cos(self.velAngr)]
    self.velvecy = [self.PosLoc[1],self.PosLoc[1]+self.PosLoc[3]*math.sin(self.velAngr)] 
    

    print("velvec angr:{:.4f}, angd:{:.4f}, vel:<{:.4f},{:.4f}>\n-> sin(ang):{:.4f} cos:{:.4f}, p:{:.4f},ang:{:.4f} from <{:.4f},{:.4f}> to <{:.4f},{:.4f}>\n".format(self.velAngr, 
                                                                                                                                self.velAngd,
                                                                                                                                self.VelRad[0],
                                                                                                                                self.VelRad[1],
                                                                                                                                math.cos(self.velAngr),
                                                                                                                                math.sin(self.velAngr),
                                                                                                                                self.pnum,self.velAngd,
                                                                                                                                self.velvecx[0],
                                                                                                                                self.velvecy[0],
                                                                                                                                self.velvecx[1],
                                                                                                                                self.velvecy[1]))
    R = [ [math.cos(self.velAngr), -math.sin(self.velAngr)],[math.sin(self.velAngr),math.cos(self.velAngr)] ]

    