
import matplotlib.pyplot as plt
from plotSphere import *
from particleData import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from plotCell import *

class BaseGenData:

    def __init__(self, FPIBGBase, ObjName,itemcfg):
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.log.logs(self,"TabFormLatex finished init.")
        self.itemcfg = itemcfg


    def Create(self):
        pass

    def run(self):
        file_name = "J:/FPIBGDATAPY/perfdataPQB/0000CollisionDataSet32X16X3.bin"
        plist = read_particle_data(file_name)
        plotParticleArray(plist,aspoints=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for ii in range(1,10):
            for jj in range(1,10):
                for kk in range(1,10):
                    self.plot_cells(ax,ii,jj,kk)
        

        plt.show(block=True)

    def plot_cells(self,ax,cx,cy,cz):
        R = 0.5
        pt_lst = np.zeros((8,3))
        pt_lst[0]= [cx-R,cy-R,cz-R]
        pt_lst[1]= [cx+R,cy-R,cz-R]
        pt_lst[2]= [cx+R,cy+R,cz-R]
        pt_lst[3]= [cx-R,cy+R,cz-R]
        pt_lst[4]= [cx-R,cy-R,cz+R]
        pt_lst[5]= [cx+R,cy-R,cz+R]
        pt_lst[6]= [cx+R,cy+R,cz+R]
        pt_lst[7]= [cx-R,cy+R,cz+R]
        x = pt_lst[:,0]
        y = pt_lst[:,1]
        z = pt_lst[:,2]
        #print(x)
        ##print(y)
        #print(z)

        # Face IDs
        vertices = [[0,1,2,3],[1,5,6,2],[3,2,6,7],[4,0,3,7],[5,4,7,6],[4,5,1,0]]


        face_color = [1.0/cx,1.0/cy,1.0/cz]
        tupleList = list(zip(x, y, z))
        poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
        #ax.plot(pt_lst[0][0],pt_lst[1][0],pt_lst[2][0])
        ax.add_collection3d(Poly3DCollection(poly3d, edgecolors= 'k',facecolors=face_color, linewidths=1, alpha=0.5))
        index = 0
        """
        for ii in pt_lst:
            label = "(num={:d}- {:2f}, {:2f}, {:2f})".format(index,ii[0],ii[1],ii[2] )
            ax.text(ii[0],ii[1],ii[2], label)
            index +=1
        """

#%******************************************************************/
#pragma once
#pdata = pycstruct.StructDef()
#pdata.add(pnum;
	#double rx;
	#double ry;
	#double rz;
	#double radius;
	#double vx;
	#double vy;
	#double vz;
	#double ptype;
	#double seq;
	#double acc_r;
	#double acc_a;
	#double molar_mass;
	#double temp_vel;
    def read_particle_data(file_name):
        struct_fmt = 'dddddddddddddd'
        #struct_fmt = 'ffffffffffffff'
        struct_len = struct.calcsize(struct_fmt)
        print(struct_len)
        struct_unpack = struct.Struct(struct_fmt).unpack_from
        count = 0
        results = []
        
        with open(file_name, "rb") as f:
            while True:
                data = f.read(struct_len)
                if not data: 
                    break
                if(len(data) < struct_len):
                    break
                s = struct_unpack(data)
                results.append(s)
        #len_data = len(results)
        #print(len_data)
        p_lst = []
        #for ii in range(4):
        #   print("partnum:{:.0f},rx:{:.2f},ry:{:.2f},rz:{:.2f}".format(results[ii][0],results[ii][1],results[ii][2],results[ii][3]))
        return np.array(results)
    
    
    def plotParticleArray(npplist,scolor=None,aspoints=True,start=0,end=None,sidelen=None):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        plotSphere(npplist,ax,scolor,aspoints,start,end)
        ax.set_title('3D Line Plot')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        if sidelen != None:
            lims = [0,sidelen]
            ax.set_xlim(lims)
            ax.set_ylim(lims)
            ax.set_zlim(lims)
        else:
            mxlims = max(npplist[:,1])
            mylims = max(npplist[:,2])
            mzlims = max(npplist[:,3])
            lims = [0,max([mxlims,mylims,mzlims])]
            ax.set_xlim(lims)
            ax.set_ylim(lims)
            ax.set_zlim(lims)
        ax.set_title('3D Sphere')
        plt.gca().set_aspect('equal')
        plt.show()
