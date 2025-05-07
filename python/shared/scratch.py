import numpy as np
import os
ary = np.zeros((20, 12),dtype=int)
print(ary)

fileName = "../CellArray{}.csv".format(0)
np.savetxt(fileName, ary, fmt='%.d', delimiter=',', newline="\r")
aryin = np.loadtxt(fileName, dtype=int, delimiter=',')
print(aryin)

