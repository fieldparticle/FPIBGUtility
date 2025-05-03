from dataclasses import dataclass,field
from typing import List,ClassVar

class CollImg:
      
    def __init__ (self,xlen,ylen,zlen):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.size = xlen*ylen*zlen
        self.maxOccupant = self.size
        self.occupancy_array = [int]*self.maxOccupant
        self.collImg = [self.occupancy_array]*self.size
        print("cells is:",self.maxOccupant, " long." )

class LockIndex:

    def __init__ (self,xlen,ylen,zlen):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.size = xlen*ylen*zlen
        self.LockImg = [int]*self.size
    

