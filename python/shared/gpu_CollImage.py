from dataclasses import dataclass,field
from typing import List,ClassVar
import atomics

class CollImg():
      
    def __init__ (self,xlen,ylen,zlen,maxOccupancy):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.maxOccupancy = maxOccupancy
        self.size = xlen*ylen*zlen
        self.loc = [[int]*self.maxOccupancy]*self.size
        print("cells is:",self.size, " long." )

class LockIndex(List):

    def __init__ (self,xlen,ylen,zlen):
        super().__init__(self)
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.size = xlen*ylen*zlen
        self = [atomics.atomic(width=4, atype=atomics.INT)]*self.size
    

