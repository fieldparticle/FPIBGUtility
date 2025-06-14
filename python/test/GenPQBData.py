
from BaseGenData import *

class GenPQBData(BaseGenData):

    def __init__(self, FPIBGBase, ObjName,itemcfg):
        super().__init__(FPIBGBase, ObjName,itemcfg)



    def gen_data(self):
        self.gen_data_base()
        self.do_cells()

    def plot_particle_cell(self):
        self.plot_particle_cell()
    
    
    def place_particles(self,xx,yy,zz,layer,row,col,w_list):
        
        if(self.particles_in_cell_count > self.particles_in_cell ):
            return 2
        
        if (self.particle_count > self.number_particles):
            return 3
        
        print(f"particle: {self.particle_count}, xx={xx}, yy= {yy}, zz={zz}, layer= {layer}, row= {row} col= {col}")
        #                         |offset so no particle is in a cell with a zero in it|
        single_particle_length  = 0.5 + self.center_line_length 

        if(self.collsions_in_cell_count <= self.num_collisions_per_cell):
            rx = single_particle_length*row - self.radius/2.0 + xx
            self.collsions_in_cell_count+=2
        else:
            rx = single_particle_length*row + xx

        ry = single_particle_length*col + yy
        rz = single_particle_length*layer + zz
        print(f"Particle Loc: <{rx:2f},{ry:2f},{rz:2f})>")

        particle_struct = pdata
        particle_struct.pnum = self.particle_count
        particle_struct.rx = rx
        particle_struct.ry = ry
        particle_struct.rz = rz
        particle_struct.radius = rx
        w_list.append(particle_struct)
        self.particle_count+=1
        self.particles_in_cell_count +=1
        return 0
        
    
    def do_cells(self):
        ret = 0
        self.w_list = []
        self.particle_count = 0
        self.open_bin_file()
        for xx in range(self.cell_x_len):
            for yy in range(self.cell_y_len):
                for zz in range(self.cell_z_len):
                    self.collsions_in_cell_count = 0
                    self.particles_in_cell_count = 0
                    # Inside a single cell. Process single cell
                    for layer in range(self.particles_in_layers):
                            for col in range(self.particles_in_col):
                                # Do row by row first so to create colsions beteen part in differnt rows
                                for row in range(self.particles_in_row):
                                    ret = self.place_particles(xx,yy,zz,layer,row,col,self.w_list)
                                    if ret == 3:
                                        return 0
                                    if len(self.w_list) >= int(self.cfg.write_block_len_text):
                                        self.write_bin_file(self.w_list)
                                        self.w_list.clear()
        self.write_bin_file(self.w_list)
        self.bin_file.close()
                                    
        
    
