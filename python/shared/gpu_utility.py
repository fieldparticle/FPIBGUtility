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

