from dataclasses import dataclass,field
from typing import List,ClassVar
from threading import Thread, Lock
import array
import pandas as pd 
import numpy as np 



class CellArray():
      
    def __init__ (self,xlen,ylen,zlen,maxOccupancy):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.maxOccupancy = maxOccupancy
        self.size = xlen*ylen*zlen
       #self.loc = [[int]*self.maxOccupancy]*self.size
        self.loc = np.zeros((self.size, self.maxOccupancy),dtype=int)
        np.zeros(shape=(3, 2))
        print("cells is:",self.size, " long." )

    def writeCellArray(self,frame):
        fileName = "../CellArray{}.csv".format(frame)
        np.savetxt(fileName, self.loc, fmt='%.d', delimiter=',', newline="\r")

    def reset(self):
        for ii in range(self.size):
            for jj in range(self.maxOccupancy):
                self.loc[ii][jj] = 0
        

class LockIndex():

    def __init__ (self,xlen,ylen,zlen):
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen
        self.size = xlen*ylen*zlen
        self.lock = [Lock()]*self.size
        self.val = array.array('i',(0 for i in range(0,self.size)))
        self.rptAtomic = False

    def reportAtomic(self,flag):
        self.rptAtomic = flag

    def reset(self):
        for ii in range(self.size):
             self.val[ii] = 0 

    def atomicAdd(self,index):
        save = self.val[index]
        self.lock[index].acquire()
        self.val[index] = self.val[index] + 1
        self.lock[index].release()

        
        if self.rptAtomic == True:
            print("Atomic add Index:{}, val before:{}, val after:{}".format(index,save,self.val[index]))

        return self.val[index]
    
        

