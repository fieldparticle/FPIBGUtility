import pytest
import os
import csv
import sys
from typing import Type

# Point ot the shared firectory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared')))
# Get the current working directory and set it to the parent directory.
cwd = os.getcwd()
os.chdir("..\\..\\") 
print(cwd)
# Import requied classes
from mock import mock, Mock
from unittest.mock import mock_open, patch
from gpu_utility import *
# Run a test. This test changes the data directory to one that does not exists 
# and tests to insure that it failes
def test_IndexingOK():
    
    
    width = 10
    height =10
    if False:
        for ii in range(100):
            locindex = ii
            ary = IndexToArray(locindex,width,height)
            print(ary)
            index = ArrayToIndex(ary,width,height,width*height)
            print(index)
            assert index == locindex
    f1 = 0.32
    f2 = 0.55
    f3 = 0.11
    if True:
        for ii in range(width):
                for jj in range(height):
                    for kk in range(width):
                        iii = ii+f1
                        jjj = jj+f2
                        kkk = kk+f3
                        locary = [iii,jjj,kkk]
                        index = ArrayToIndex(locary,width,height,width*height*height)
                        print("(",int(iii),int(jjj),int(kkk),")","(",iii,jjj,kkk,")=",index)

        # Assert that the log line with the correct code was written to the log file
    #assert dataClass.log.CheckLogFile("1001") == True
    

