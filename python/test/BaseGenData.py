import struct
import os
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import ctypes
import math
from abc import ABC, abstractmethod
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
class pdata(ctypes.Structure):
    _fields_ = [("pnum", ctypes.c_double),
                ("rx",  ctypes.c_double),
                ("ry",  ctypes.c_double),
                ("rz",  ctypes.c_double),
                ("radius",  ctypes.c_double),
                ("vx",  ctypes.c_double),
                ("vy",  ctypes.c_double),
                ("vz",  ctypes.c_double),
                ("ptype",  ctypes.c_double),
                ("seq",  ctypes.c_double),
                ("acc_r",  ctypes.c_double),
                ("Acc_a",  ctypes.c_double),
                ("molar_mass",  ctypes.c_double),
                ("temp_vel",  ctypes.c_double)]          
          


class BaseGenData:

    particle_list = []
    particle_count = 0
    collision_count = 0
    collsions_in_cell_count = 0
    particles_in_cell_count = 0
    select_list = []
    sepdist = 0.05
    bin_file = None
    def __init__(self, FPIBGBase, ObjName,itemcfg):
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.log.logs(self,"TabFormLatex finished init.")
        self.itemcfg = itemcfg
        self.cfg = self.itemcfg.config

    @abstractmethod
    def gen_data(self):
        pass
    @abstractmethod
    def plot_particle_cell(self):
        pass

    @abstractmethod
    def place_particles(self,row,column):
        pass
    
    @abstractmethod
    def do_cells(self):
        pass
    
    
    def open_bin_file(self):
         self.bin_file = open(self.test_bin_name,"wb")

    def write_bin_file(self,w_lst):
        for ii in w_lst:
            self.bin_file.write(w_lst)
        

    def write_test_file(self):
        if not os.path.exists(os.path.isdir(self.cfg.data_dir)):
            os.makedirs(os.path.isdir(self.cfg.data_dir))

    def calc_test_parms(self):
        pass

    # load all lines from the particle selections file into selections list
    def open_selections_file(self):
        try:
            with open(self.cfg.selections_file_text,"r",newline='') as csvfl:
                reader = csv.DictReader(csvfl, delimiter=',',dialect='excel')
                for row in reader:
                    if row["sel"] == 's':
                        self.select_list.append(row)
                        return
                        
        except BaseException as e:
            print(e)



        
    def calulate_cell_properties(self,index,sel_dict):
        self.collision_density           = float(sel_dict['cdens'])
        self.number_particles       =  int(sel_dict['tot'])
        self.radius                 = float(sel_dict['radius'])
        self.sepdist                =  float(self.cfg.particle_separation_text)
        self.center_line_length          = 2*self.radius  + self.radius*self.sepdist
        self.particles_in_row       = int(math.floor(1.00 /self.center_line_length))
        self.particles_in_col       = int(math.floor(1.00 /self.center_line_length))
        self.particles_in_layers    = int(math.floor(1.00 /self.center_line_length))
        self.particles_in_cell      = self.particles_in_row*self.particles_in_col*self.particles_in_layers
        self.particles_in_space	    = int(self.particles_in_row*self.particles_in_col*self.particles_in_layers)
        # Somtimes we do very small number of particles to check the pattern
        if (self.particles_in_space > self.number_particles):
            self.particles_in_space = self.number_particles
        self.cell_array_size      = self.particles_in_space+10
        self.num_collisions_per_cell = math.ceil(self.particles_in_space * self.collision_density/2.0)
        # Calulate side length based on particles per cell
        side_len = 0
        while True:
            side_len += 1
            if (side_len * side_len * side_len * self.particles_in_space >= self.number_particles):
                break
        self.side_length = side_len
        self.cell_x_len = self.side_length+1
        self.cell_y_len = self.side_length+1
        self.cell_z_len = self.side_length+1
        self.tot_num_cells = self.number_particles / self.particles_in_space
        self.tot_num_collsions = math.ceil(int(self.tot_num_cells *self.num_collisions_per_cell*2.0 ))
        self.set_file_name = "{:03d}CollisionDataSet{:d}X{:d}X{:d}".format(index,self.number_particles,self.tot_num_collsions,side_len)
        self.test_file_name = self.cfg.data_dir + '/' + self.set_file_name + '.tst'
        self.test_bin_name = self.cfg.data_dir + '/' + self.set_file_name + '.bin'
        self.report_file = self.cfg.data_dir + '/' + self.set_file_name

        print(f"Collsion Density: { self.collision_density},Number particles:{self.number_particles},Radius: {self.radius}, Separation Dist: {self.sepdist }, Center line length: {self.center_line_length:.2f}")
        print(f"Particles in row: {self.particles_in_row}, Particles in Column: {self.particles_in_col}, Particles per cell: {self.particles_in_cell}")
        print(f"Particles in space: {self.particles_in_space}, Cell array size: {self.cell_array_size }")

    def write_test_file(self,index,sel_dict):
        
        with open(self.test_file_name,'w') as f:
            fstr = f"index = {index}\n"     
            f.write(fstr)
            fstr = f"CellAryW = {self.cell_x_len+1}\n"     
            f.write(fstr)
            fstr = f"CellAryH = {self.cell_y_len+1}\n"     
            f.write(fstr)
            fstr = f"CellAryL = {self.cell_z_len+1}\n"     
            f.write(fstr)
            fstr = f"radius = {self.radius}\n"
            f.write(fstr)
            fstr = f"PartPerCell = {self.particles_in_space}\n"
            f.write(fstr)
            fstr = f"pcount = {self.number_particles}\n"
            f.write(fstr)
            fstr = f"colcount = {self.tot_num_collsions}\n"
            f.write(fstr)
            fstr = f"dataFile = {self.test_bin_name}\n"
            f.write(fstr)
            fstr = f"aprFile = { self.report_file}\n"
            f.write(fstr)
            fstr = f"density = {sel_dict['cdens']}\n"
            f.write(fstr)
            fstr = f"pdensity = 0\n"
            f.write(fstr)
            fstr = f"dispatchx = {sel_dict['wx']}\n"
            f.write(fstr)
            fstr = f"dispatchx = {sel_dict['wy']}\n"
            f.write(fstr)
            fstr = f"dispatchx = {sel_dict['wz']}\n"
            f.write(fstr)
            fstr = f"dispatchx = {sel_dict['dx']}\n"
            f.write(fstr)
            fstr = f"dispatchx = {sel_dict['dx']}\n"
            f.write(fstr)
            fstr = f"dispatchx = {sel_dict['dz']}\n"
            f.write(fstr)
            fstr = f"ColArySize = {self.cell_array_size}\n"
            f.write(fstr)



    def gen_data_base(self):
        if not os.path.exists(self.cfg.data_dir):
            os.makedirs(self.cfg.data_dir)
        # Scan each line of the selections list, calulate properties, and gen data
        self.open_selections_file()
        index = 0
        
        for ii in self.select_list:
            self.calulate_cell_properties(index,ii)
            self.write_test_file(index,ii)
            index+=1
        self.select_list.clear()

    def plot_particle_cell_base(self):
        file_name = "J:/FPIBGDATAPY/perfdataPQB/0000CollisionDataSet32X16X3.bin"
        plist = self.read_particle_data(file_name)
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.plotParticleArray(plist,aspoints=False)
        for ii in range(1,10):
            for jj in range(1,10):
                for kk in range(1,10):
                    self.plot_cells(ii,jj,kk)
        

        plt.show(block=True)

    def plot_cells(self,cx,cy,cz):
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
        # Face IDs
        vertices = [[0,1,2,3],[1,5,6,2],[3,2,6,7],[4,0,3,7],[5,4,7,6],[4,5,1,0]]
        face_color = [1.0/cx,1.0/cy,1.0/cz]
        tupleList = list(zip(x, y, z))
        poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
        #ax.plot(pt_lst[0][0],pt_lst[1][0],pt_lst[2][0])
        self.ax.add_collection3d(Poly3DCollection(poly3d, edgecolors= 'k',facecolors=face_color, linewidths=1, alpha=0.5))
     

    def read_particle_data(self,file_name):
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
    
    
    def plotParticleArray(self,npplist,scolor=None,aspoints=True,start=0,end=None,sidelen=None):
    
        self.plotSphere(npplist,scolor,aspoints,start,end)
        self.ax.set_title('3D Line Plot')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        if sidelen != None:
            lims = [0,sidelen]
            self.ax.set_xlim(lims)
            self.ax.set_ylim(lims)
            self.ax.set_zlim(lims)
        else:
            mxlims = max(npplist[:,1])
            mylims = max(npplist[:,2])
            mzlims = max(npplist[:,3])
            lims = [0,max([mxlims,mylims,mzlims])]
            self.ax.set_xlim(lims)
            self.ax.set_ylim(lims)
            self.ax.set_zlim(lims)
        self.ax.set_title('3D Sphere')
        plt.gca().set_aspect('equal')
        
