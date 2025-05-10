
import math
import numpy as np 
def IndexToArray(index, width, height):
	
    c1=0
    c2=0
    c3=0
    width = width
    height=height
    w = width+1
    h = height+1
    c1 = index / (w * h)
    c2 = (index - c1 * w * h) / w
    c3 = index - w * (c2 + w * c1)
    
    locvect = []
    locvect.append(c3)
    locvect.append(c2)
    locvect.append(c1)
    return locvect

def ArrayToIndex(locary,width,height,maxLocation):
    w = width+1
    h = height+1
    x = 0
    indxLoc =  int(locary[0]) + w * int(locary[1]) + h * int(locary[2])
    #indxLoc = int(locary[0])*(width*height)+int(locary[1])*width+int(locary[2])
    if(indxLoc > maxLocation-1):
        errtxt = "gpu_utility-><{},{},{}> at {} excceds maxloc at {}".format(locary[0],locary[1],locary[2],indxLoc,maxLocation-1)
        print(errtxt)
        return 0
    else:
        return indxLoc
    


def angle_to(p1, p2, rotation=0, clockwise=False):
    angle = math.radians(math.atan2(p2[1] - p1[1], p2[0] - p1[0])) - rotation
    if not clockwise:
        angle = -angle
    return angle % 2*math.pi


def atan2o(dx,dy):
    if dx==0:
        if dy>0:
            theta=0
        else:
            theta=math.pi
    
    elif dy==0:
        if dx>0:
            theta=math.pi/2
        else:
            theta=-math.pi/2
    
    elif dx>0:
        if dy>0:
            theta=math.atan(dx/dy)
        else:
            theta=math.pi+math.atan(dx/dy)
   
    elif dx<0:
        if dy>0:
            theta=math.atan(dx/dy)
        else:
            theta=math.atan(dx/dy)-math.pi

    return -theta+math.pi

